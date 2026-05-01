"""
Optimization endpoints — uses OSRM for routing and distance matrices.
The movement profile (driving | cycling | walking) is resolved from the
request payload and applied consistently to all OSRM calls.
"""
from typing import List, Dict
import math
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.permissions import require_roles
from app.models.user import User
from app.models.optimization_job import OptimizationJob
from app.schemas.route import OptimizeRequest, OptimizeResponse, ProfilesResponse, ProfileInfo
from app.services.osrm_service import get_matrix, get_route
from app.services.movement_profiles import resolve_profile, get_profile_metadata, VALID_PROFILES, PROFILE_LABELS
from datetime import datetime, timezone, timedelta

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


@router.get("/profiles", response_model=ProfilesResponse, status_code=status.HTTP_200_OK)
async def list_profiles():
    """
    Return all available movement profiles with labels and icons.
    The frontend uses this to populate the mode selector UI.
    """
    profiles = [
        ProfileInfo(
            key=key,
            label=meta["label"],
            icon=meta["icon"],
            description=meta["description"],
        )
        for key, meta in PROFILE_LABELS.items()
    ]
    return ProfilesResponse(profiles=profiles)


@router.post("/", response_model=OptimizeResponse, status_code=status.HTTP_200_OK)
async def submit_optimization(
    payload: OptimizeRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(["admin", "manager", "driver"])),
):
    """
    Optimization endpoint using OSRM.
    1. Resolves the movement profile from the request.
    2. Gets distance/duration matrix from OSRM using that profile.
    3. Runs Nearest Neighbor TSP to order the stops.
    4. Fetches the exact route geometry for the ordered stops from OSRM.
    5. Calculates ETAs from the OSRM leg durations (not static speeds).
    6. Returns geometry, stops, timings, and the resolved profile metadata.
    """
    locations_dict = [loc.model_dump() for loc in payload.locations]
    num_stops = len(locations_dict)
    
    if num_stops < 2:
        raise HTTPException(status_code=400, detail="At least 2 locations required.")

    # Resolve the movement profile — this is the single call that determines
    # which OSRM profile is used for the entire optimization pipeline.
    profile = resolve_profile(explicit_profile=payload.profile, vehicle_type=None)
    profile_meta = get_profile_metadata(profile)

    # 1. Fetch Matrix using the resolved profile (OSRM durations vary by mode)
    if num_stops > 50:
        durations = calculate_haversine_matrix(locations_dict)
    else:
        try:
            matrix_data = await get_matrix(locations_dict, profile=profile)
            durations = matrix_data.get("durations", [])
            if not durations or len(durations) != num_stops:
                durations = calculate_haversine_matrix(locations_dict)
        except HTTPException:
            durations = calculate_haversine_matrix(locations_dict)

    # 2. Run Nearest Neighbor Optimization (profile-aware because durations reflect real travel times)
    optimized_indices = nearest_neighbor_tsp(durations, num_stops)
    
    # 3. Reorder locations based on TSP
    ordered_locations = [locations_dict[i] for i in optimized_indices]
    
    # 4. Fetch final route details (distance, duration, geometry) with the same profile
    total_distance = 0.0
    total_duration = 0.0
    leaflet_geometry = []
    best_route = {}

    # Chunking route calls if too many stops (e.g. > 50)
    chunk_size = 50
    chunks = []
    for i in range(0, num_stops, chunk_size - 1):
        chunk = ordered_locations[i:i + chunk_size]
        if len(chunk) > 1:
            chunks.append(chunk)
            
    if not chunks and num_stops == 1:
        leaflet_geometry = [[ordered_locations[0]["latitude"], ordered_locations[0]["longitude"]]]
        
    for chunk in chunks:
        try:
            # Use the same profile for route geometry — ensures displayed path matches mode
            route_data = await get_route(chunk, profile=profile)
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
            chunk_geom = [[loc["latitude"], loc["longitude"]] for loc in chunk]
            if leaflet_geometry and chunk_geom:
                leaflet_geometry.extend(chunk_geom[1:])
            else:
                leaflet_geometry.extend(chunk_geom)
            for i in range(len(chunk)-1):
                dist = haversine_distance(chunk[i], chunk[i+1])
                total_distance += dist
                total_duration += dist / 10.0
    
    # 5. Calculate ETAs using actual OSRM leg durations (profile-accurate times)
    current_eta = datetime.now(timezone.utc)
    response_stops = []
    
    # Use legs from the single chunk case for accurate per-stop ETAs
    use_actual_legs = len(chunks) == 1 and "legs" in best_route
    legs = best_route.get("legs", []) if use_actual_legs else []
    
    for seq_num, loc in enumerate(ordered_locations, start=1):
        response_stops.append({
            "sequence": seq_num,
            "latitude": loc["latitude"],
            "longitude": loc["longitude"],
            "address": loc.get("address", f"Stop {seq_num}"),
            "status": "pending",
            "eta": current_eta.isoformat()
        })
        
        # Advance ETA using OSRM leg durations, which already reflect the movement profile
        if use_actual_legs and seq_num - 1 < len(legs):
            leg_duration = legs[seq_num - 1].get("duration", 0.0)
            current_eta += timedelta(seconds=leg_duration + 600)  # 10 min service time
        else:
            current_eta += timedelta(seconds=(total_duration / max(1, num_stops - 1)) + 600)

    # 6. Log the job in history
    job = OptimizationJob(
        org_id=current_user.org_id,
        owner_id=current_user.id,
        status="completed",
        algorithm=payload.algorithm,
        profile=profile,
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
        "duration": total_duration,
        "profile": profile,
        "profile_label": profile_meta["label"],
        "profile_icon": profile_meta["icon"],
    }


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

