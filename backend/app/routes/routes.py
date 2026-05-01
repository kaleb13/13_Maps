"""
Route management endpoints.
"""
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.core.permissions import require_roles
from app.models.user import User
from app.models.route import Route, RouteStop
from app.models.job import Job
from app.schemas.route import RouteCreate, RouteResponse, RouteListResponse
from app.services.mock_optimizer import MockOptimizer
from app.services.geocoding import GeocodingService
from app.services.route_optimization import RouteOptimizationService

router = APIRouter()


@router.post("/", response_model=RouteResponse, status_code=status.HTTP_201_CREATED)
async def create_route(
    payload: RouteCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(["admin", "manager"])),
):
    """
    Create a new route with a list of locations and immediately perform mock optimization.
    Requires Manager or Admin role.
    """
    # 1. Run mock optimization on the raw locations
    locations_dict = [loc.model_dump() for loc in payload.locations]
    optimized_data = MockOptimizer.optimize(locations_dict)
    
    # 2. Create the Route header
    route = Route(
        name=payload.name,
        org_id=current_user.org_id,
        created_by_id=current_user.id,
        total_distance_m=optimized_data["distance"],
        total_duration_s=optimized_data["duration"],
        stop_count=len(optimized_data["stops"]),
        status="optimized"
    )
    db.add(route)
    await db.flush()

    # 3. Create Jobs and RouteStops for each optimized location
    response_stops = []
    for stop_data in optimized_data["stops"]:
        address = stop_data.get("address", "Unknown Location")
        if address == "Unknown Location" or str(address).startswith("Stop "):
            try:
                geo = await GeocodingService.reverse_geocode(stop_data["latitude"], stop_data["longitude"])
                if geo and geo.get("display_name"):
                    address = geo["display_name"]
            except Exception:
                pass
                
        # Create a Job (delivery point) for the stop
        job = Job(
            org_id=current_user.org_id,
            title=address,
            address=address,
            latitude=stop_data["latitude"],
            longitude=stop_data["longitude"],
            status="assigned"
        )
        db.add(job)
        await db.flush()
        
        # Create the RouteStop linking the Route and the Job
        route_stop = RouteStop(
            route_id=route.id,
            job_id=job.id,
            sequence=stop_data["sequence"],
            status="pending"
        )
        db.add(route_stop)
        await db.flush()
        
        # Build the response stop object manually since the DB relationships 
        # might not be fully loaded/accessible without a refresh and joinedload.
        response_stops.append({
            "id": route_stop.id,
            "sequence": route_stop.sequence,
            "latitude": job.latitude,
            "longitude": job.longitude,
            "address": job.address,
            "status": route_stop.status,
            "estimated_arrival": None
        })

    await db.commit()

    return {
        "route_id": route.id,
        "name": route.name,
        "status": route.status,
        "distance": route.total_distance_m,
        "duration": route.total_duration_s,
        "stops": response_stops
    }


@router.get("/", response_model=List[RouteListResponse])
async def list_routes(
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(["admin", "manager", "driver"])),
):
    """
    Get all routes belonging to the organization.
    Drivers can theoretically only see their own, but for now we filter by org.
    """
    query = select(Route).where(Route.org_id == current_user.org_id)
    
    # If driver, strictly filter by assigned routes (if driver_id was set)
    if current_user.role == "driver":
        query = query.where(Route.driver_id == current_user.id)
        
    result = await db.execute(query.offset(skip).limit(limit))
    return result.scalars().all()


@router.get("/{route_id}", response_model=RouteResponse)
async def get_route(
    route_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(["admin", "manager", "driver"])),
):
    """
    Get a specific route by ID, including its stops and coordinates.
    """
    query = select(Route).options(
        selectinload(Route.stops).selectinload(RouteStop.job)
    ).where(
        Route.id == route_id,
        Route.org_id == current_user.org_id,
    )
    
    if current_user.role == "driver":
        query = query.where(Route.driver_id == current_user.id)
        
    result = await db.execute(query)
    route = result.scalar_one_or_none()
    
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
        
    response_stops = []
    for stop in route.stops:
        response_stops.append({
            "id": stop.id,
            "sequence": stop.sequence,
            "latitude": stop.job.latitude,
            "longitude": stop.job.longitude,
            "address": stop.job.address,
            "status": stop.status,
            "estimated_arrival": stop.estimated_arrival
        })
        
    return {
        "route_id": route.id,
        "name": route.name,
        "status": route.status,
        "distance": route.total_distance_m or 0.0,
        "duration": route.total_duration_s or 0.0,
        "stops": response_stops
    }


@router.delete("/{route_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_route(
    route_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(["admin", "manager"])),
):
    """
    Delete a route. Requires Manager or Admin role.
    """
    result = await db.execute(
        select(Route).where(
            Route.id == route_id,
            Route.org_id == current_user.org_id,
        )
    )
    route = result.scalar_one_or_none()
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
        
    await db.delete(route)
    await db.commit()

@router.post("/{route_id}/optimize")
async def optimize_existing_route(
    route_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(["admin", "manager"])),
):
    """
    Optimize an existing route:
    1. Uses OSRM to determine the best sequence and durations.
    2. Calculates accurate ETA for each stop.
    3. Updates RouteStops and Route records in the database.
    """
    try:
        # The logic is encapsulated in the service layer
        result = await RouteOptimizationService.optimize_route_record(route_id, current_user.org_id, db)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
