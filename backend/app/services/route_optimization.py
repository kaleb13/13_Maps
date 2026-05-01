from typing import List, Dict, Any
from datetime import datetime, timezone, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException

from app.models.route import Route, RouteStop
from app.services.osrm_service import get_matrix, get_route
import math

class RouteOptimizationService:
    
    @staticmethod
    def haversine_distance(loc1: Dict, loc2: Dict) -> float:
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

    @staticmethod
    def calculate_haversine_matrix(locations: List[Dict]) -> List[List[float]]:
        num_stops = len(locations)
        matrix = [[0.0] * num_stops for _ in range(num_stops)]
        for i in range(num_stops):
            for j in range(num_stops):
                if i != j:
                    matrix[i][j] = RouteOptimizationService.haversine_distance(locations[i], locations[j])
        return matrix

    @staticmethod
    def nearest_neighbor_tsp(durations: List[List[float]], num_stops: int) -> List[int]:
        unvisited = set(range(1, num_stops))
        path = [0]
        current = 0
        while unvisited:
            next_node = min(unvisited, key=lambda node: durations[current][node])
            path.append(next_node)
            unvisited.remove(next_node)
            current = next_node
        return path

    @staticmethod
    async def optimize_route_record(route_id: str, org_id: str, db: AsyncSession) -> Dict[str, Any]:
        # Fetch route with stops and jobs
        query = select(Route).options(
            selectinload(Route.stops).selectinload(RouteStop.job)
        ).where(
            Route.id == route_id,
            Route.org_id == org_id
        )
        result = await db.execute(query)
        route = result.scalar_one_or_none()
        
        if not route:
            raise HTTPException(status_code=404, detail="Route not found")
            
        if not route.stops or len(route.stops) < 2:
            raise HTTPException(status_code=400, detail="Route must have at least 2 stops to optimize")

        # Prepare locations dicts
        locations_dict = []
        for stop in route.stops:
            locations_dict.append({
                "stop_id": stop.id,
                "job_id": stop.job.id,
                "latitude": stop.job.latitude,
                "longitude": stop.job.longitude,
                "address": stop.job.address,
                "original_stop": stop
            })
            
        num_stops = len(locations_dict)
        
        # Get matrix and run TSP
        if num_stops > 50:
            durations = RouteOptimizationService.calculate_haversine_matrix(locations_dict)
        else:
            try:
                matrix_data = await get_matrix(locations_dict, profile=route.profile)
                durations = matrix_data.get("durations", [])
                if not durations or len(durations) != num_stops:
                    durations = RouteOptimizationService.calculate_haversine_matrix(locations_dict)
            except Exception:
                durations = RouteOptimizationService.calculate_haversine_matrix(locations_dict)
                
        optimized_indices = RouteOptimizationService.nearest_neighbor_tsp(durations, num_stops)
        ordered_locations = [locations_dict[i] for i in optimized_indices]
        
        # Get final route and legs
        try:
            route_data = await get_route(ordered_locations, profile=route.profile)
            osrm_routes = route_data.get("routes", [])
            if not osrm_routes:
                raise ValueError("No route returned by OSRM")
            best_route = osrm_routes[0]
            total_distance = best_route.get("distance", 0.0)
            total_duration = best_route.get("duration", 0.0)
            legs = best_route.get("legs", [])
        except Exception:
            # Fallback if get_route fails
            total_distance = 0.0
            total_duration = 0.0
            legs = []
            for i in range(len(ordered_locations) - 1):
                dist = RouteOptimizationService.haversine_distance(ordered_locations[i], ordered_locations[i+1])
                total_distance += dist
                total_duration += dist / 10.0
                legs.append({"duration": dist / 10.0})

        # Calculate ETAs
        # Start time is departure_time (time), need to combine with scheduled_date or today
        if route.scheduled_date and route.departure_time:
            start_dt = datetime.combine(route.scheduled_date, route.departure_time).replace(tzinfo=timezone.utc)
        else:
            start_dt = datetime.now(timezone.utc)

        current_eta = start_dt
        response_stops = []
        
        for i, loc in enumerate(ordered_locations):
            stop = loc["original_stop"]
            stop.sequence = i + 1
            stop.estimated_arrival = current_eta
            
            response_stops.append({
                "sequence": stop.sequence,
                "address": loc["address"],
                "eta": current_eta.isoformat()
            })
            
            if i < len(legs):
                # Add duration to reach the next stop
                leg_duration = legs[i].get("duration", 0.0)
                # also consider service time (from job), default 10 min
                service_time = stop.job.service_time_min * 60
                current_eta = current_eta + timedelta(seconds=leg_duration + service_time)

        # Update Route record
        route.total_distance_m = total_distance
        route.total_duration_s = total_duration
        route.status = "optimized"
        
        await db.commit()
        await db.refresh(route)
        
        return {
            "route_id": route.id,
            "distance_m": total_distance,
            "duration_s": total_duration,
            "stops": response_stops
        }
