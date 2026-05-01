"""
Optimization endpoints — uses OSRM for routing and distance matrices.
"""
from typing import List, Dict
import math
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.permissions import require_roles
from app.models.user import User
from app.models.optimization_job import OptimizationJob
from app.schemas.route import OptimizeRequest, OptimizeResponse
from app.services.osrm_service import get_matrix, get_route
from datetime import datetime, timezone

router = APIRouter()

def haversine_distance(loc1: Dict, loc2: Dict) -> float:
    """Calculate distance in meters between two dicts with 'latitude' and 'longitude'."""
    R = 6371000
    lat1 = math.radians(loc1["latitude"])
    lon1 = math.radians(loc1["longitude"])
    lat2 = math.radians(loc2["latitude"])
    lon2 = math.radians(loc2["longitude"])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def calculate_haversine_matrix(locations: List[Dict]) -> List[List[float]]:
    """Generate a distance matrix using Haversine formula."""
    num_stops = len(locations)
    matrix = [[0.0] * num_stops for _ in range(num_stops)]
    for i in range(num_stops):
        for j in range(num_stops):
            if i != j:
                matrix[i][j] = haversine_distance(locations[i], locations[j])
    return matrix


def nearest_neighbor_tsp(durations: List[List[float]], num_stops: int) -> List[int]:
    """
    Very simple Nearest Neighbor heuristic for TSP.
    Starts at index 0, always visits the closest unvisited node.
    """
    unvisited = set(range(1, num_stops))
    path = [0]
    current = 0
    
    while unvisited:
        next_node = min(unvisited, key=lambda node: durations[current][node])
        path.append(next_node)
        unvisited.remove(next_node)
        current = next_node
        
    return path


@router.post("/", response_model=OptimizeResponse, status_code=status.HTTP_200_OK)
async def submit_optimization(
    payload: OptimizeRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(["admin", "manager", "driver"])),
):
    """
    Optimization endpoint using OSRM.
    1. Gets distance/duration matrix from OSRM.
    2. Runs Nearest Neighbor to order the stops.
    3. Fetches the exact route geometry for the new order from OSRM.
    """
    locations_dict = [loc.model_dump() for loc in payload.locations]
    num_stops = len(locations_dict)
    
    if num_stops < 2:
        raise HTTPException(status_code=400, detail="At least 2 locations required.")

    # 1. Fetch Matrix (Use OSRM, fallback to Haversine if too many stops)
    if num_stops > 50:
        durations = calculate_haversine_matrix(locations_dict)
    else:
        try:
            matrix_data = await get_matrix(locations_dict)
            durations = matrix_data.get("durations", [])
            if not durations or len(durations) != num_stops:
                durations = calculate_haversine_matrix(locations_dict)
        except HTTPException:
            durations = calculate_haversine_matrix(locations_dict)

    # 2. Run Nearest Neighbor Optimization
    optimized_indices = nearest_neighbor_tsp(durations, num_stops)
    
    # 3. Reorder locations based on TSP
    ordered_locations = [locations_dict[i] for i in optimized_indices]
    
    # 4. Fetch final route details (distance, duration, geometry)
    total_distance = 0.0
    total_duration = 0.0
    leaflet_geometry = []
    
    # Chunking route calls if too many stops (e.g. > 50)
    chunk_size = 50
    chunks = []
    for i in range(0, num_stops, chunk_size - 1):
        chunk = ordered_locations[i:i + chunk_size]
        if len(chunk) > 1:
            chunks.append(chunk)
            
    if not chunks and num_stops == 1:
        # Edge case: fallback or only 1 point
        leaflet_geometry = [[ordered_locations[0]["latitude"], ordered_locations[0]["longitude"]]]
        
    for chunk in chunks:
        try:
            route_data = await get_route(chunk)
            routes = route_data.get("routes", [])
            if routes:
                best_route = routes[0]
                total_distance += best_route.get("distance", 0.0)
                total_duration += best_route.get("duration", 0.0)
                
                geometry_coords = best_route.get("geometry", {}).get("coordinates", [])
                chunk_geom = [[coord[1], coord[0]] for coord in geometry_coords]
                if leaflet_geometry and chunk_geom:
                    leaflet_geometry.extend(chunk_geom[1:])
                else:
                    leaflet_geometry.extend(chunk_geom)
        except HTTPException:
            # Fallback to straight lines for this chunk
            chunk_geom = [[loc["latitude"], loc["longitude"]] for loc in chunk]
            if leaflet_geometry and chunk_geom:
                leaflet_geometry.extend(chunk_geom[1:])
            else:
                leaflet_geometry.extend(chunk_geom)
            for i in range(len(chunk)-1):
                dist = haversine_distance(chunk[i], chunk[i+1])
                total_distance += dist
                total_duration += dist / 10.0 # assume 10 m/s
    
    # Build stops response
    response_stops = []
    for seq_num, loc in enumerate(ordered_locations, start=1):
        response_stops.append({
            "sequence": seq_num,
            "latitude": loc["latitude"],
            "longitude": loc["longitude"],
            "address": loc.get("address", f"Stop {seq_num}"),
            "status": "pending"
        })

    # 5. Log the job in history
    job = OptimizationJob(
        org_id=current_user.org_id,
        owner_id=current_user.id,
        status="completed",
        algorithm=payload.algorithm,
        profile=payload.profile,
        total_distance_m=total_distance,
        total_duration_s=total_duration,
        completed_at=datetime.now(timezone.utc)
    )
    db.add(job)
    await db.commit()

    return {
        "route_id": None,
        "stops": response_stops,
        "geometry": leaflet_geometry,
        "distance": total_distance,
        "duration": total_duration
    }
