"""
Mock optimization service — returns fake optimized route data.
"""
from typing import List
import math

class MockOptimizer:
    @staticmethod
    def optimize(locations: List[dict]) -> dict:
        """
        Takes a list of location dicts: {"latitude": ..., "longitude": ..., "address": ...}
        Returns a fake optimized route.
        """
        # Fake "Nearest Neighbor" - just reverse the middle elements or sort by lat
        # For a truly simple mock, we just return them in order but calculate fake distance.
        
        optimized_stops = []
        total_distance = 0.0
        total_duration = 0.0
        
        # Simple mock: order by longitude
        sorted_locations = sorted(locations, key=lambda x: x["longitude"])
        
        for i, loc in enumerate(sorted_locations):
            stop = {
                "sequence": i + 1,
                "latitude": loc["latitude"],
                "longitude": loc["longitude"],
                "address": loc.get("address", f"Stop {i+1}"),
                "status": "pending"
            }
            optimized_stops.append(stop)
            
            # Add some fake distance/duration
            if i > 0:
                # Rough euclidean distance to meters (very fake)
                prev = sorted_locations[i-1]
                dx = loc["longitude"] - prev["longitude"]
                dy = loc["latitude"] - prev["latitude"]
                dist = math.sqrt(dx*dx + dy*dy) * 111000  # roughly meters
                total_distance += dist
                # Assume 30 km/h average speed in city
                total_duration += (dist / 1000) / 30 * 3600

        return {
            "stops": optimized_stops,
            "distance": round(total_distance, 2),
            "duration": round(total_duration, 2)
        }
