import logging
from typing import List, Dict, Any

import httpx
from fastapi import HTTPException

from app.core.config import settings

logger = logging.getLogger(__name__)

def _build_coords_string(coordinates: List[Dict[str, float]]) -> str:
    """Convert a list of {'latitude': x, 'longitude': y} to OSRM string."""
    return ";".join(f"{loc['longitude']},{loc['latitude']}" for loc in coordinates)

async def get_matrix(coordinates: List[Dict[str, float]], profile: str = "driving") -> Dict[str, Any]:
    """
    Call OSRM /table endpoint to get the distance/duration matrix.
    """
    coords = _build_coords_string(coordinates)
    url = f"{settings.OSRM_BASE_URL}/table/v1/{profile}/{coords}?annotations=duration,distance"
    
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            return resp.json()
    except httpx.HTTPStatusError as exc:
        logger.error(f"OSRM /table error: {exc.response.text}")
        raise HTTPException(status_code=400, detail="Invalid coordinates or routing failed.")
    except httpx.RequestError as exc:
        logger.error(f"OSRM connection error: {exc}")
        raise HTTPException(status_code=503, detail="Routing engine unavailable.")

async def get_route(coordinates: List[Dict[str, float]], profile: str = "driving") -> Dict[str, Any]:
    """
    Call OSRM /route endpoint to get the exact path, distance, and duration.
    """
    coords = _build_coords_string(coordinates)
    url = f"{settings.OSRM_BASE_URL}/route/v1/{profile}/{coords}?overview=full&geometries=geojson"
    
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            return resp.json()
    except httpx.HTTPStatusError as exc:
        logger.error(f"OSRM /route error: {exc.response.text}")
        raise HTTPException(status_code=400, detail="Invalid route coordinates.")
    except httpx.RequestError as exc:
        logger.error(f"OSRM connection error: {exc}")
        raise HTTPException(status_code=503, detail="Routing engine unavailable.")
