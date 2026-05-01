import httpx
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

# Simple in-memory cache to prevent duplicate requests
_cache: Dict[str, Any] = {}

class GeocodingService:
    BASE_URL = "https://nominatim.openstreetmap.org"
    HEADERS = {
        "User-Agent": "RouteOpt/1.0 (admin@addisexpress.et)"
    }

    @classmethod
    async def _request(cls, endpoint: str, params: dict) -> Any:
        # Create a cache key based on endpoint and params
        cache_key = f"{endpoint}?{'&'.join(f'{k}={v}' for k, v in sorted(params.items()))}"
        
        if cache_key in _cache:
            return _cache[cache_key]

        async with httpx.AsyncClient(headers=cls.HEADERS) as client:
            try:
                response = await client.get(f"{cls.BASE_URL}{endpoint}", params=params, timeout=10.0)
                response.raise_for_status()
                data = response.json()
                
                # Cache the result
                _cache[cache_key] = data
                return data
            except httpx.HTTPStatusError as e:
                logger.error(f"Geocoding API HTTP error: {str(e)}")
                raise ValueError(f"Geocoding service returned HTTP error: {e.response.status_code}")
            except httpx.RequestError as e:
                logger.error(f"Geocoding API request error: {str(e)}")
                raise ValueError(f"Geocoding service unavailable: {str(e)}")
            except Exception as e:
                logger.error(f"Unexpected geocoding error: {str(e)}")
                raise ValueError(f"Unexpected error: {str(e)}")

    @classmethod
    async def forward_geocode(cls, query: str) -> Optional[Dict[str, Any]]:
        params = {
            "q": query,
            "format": "json",
            "limit": 1
        }
        
        data = await cls._request("/search", params)
        
        if not data or len(data) == 0:
            return None
            
        result = data[0]
        return {
            "lat": float(result["lat"]),
            "lon": float(result["lon"]),
            "display_name": result["display_name"]
        }

    @classmethod
    async def reverse_geocode(cls, lat: float, lon: float) -> Optional[Dict[str, Any]]:
        params = {
            "lat": lat,
            "lon": lon,
            "format": "json"
        }
        
        data = await cls._request("/reverse", params)
        
        if not data or "error" in data:
            return None
            
        return {
            "display_name": data.get("display_name", "Unknown Location")
        }
