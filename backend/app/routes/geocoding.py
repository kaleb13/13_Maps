from fastapi import APIRouter, HTTPException, Query
from app.services.geocoding import GeocodingService
from pydantic import BaseModel

router = APIRouter()

class ForwardResponse(BaseModel):
    lat: float
    lon: float
    display_name: str

class ReverseResponse(BaseModel):
    display_name: str

@router.get("/search", response_model=ForwardResponse)
async def forward_geocode(q: str = Query(..., description="The address or place name to search for")):
    """
    Convert an address or place name into geographic coordinates.
    """
    try:
        result = await GeocodingService.forward_geocode(q)
        if not result:
            raise HTTPException(status_code=404, detail=f"No location found for query: '{q}'")
        return result
    except ValueError as e:
        raise HTTPException(status_code=502, detail=str(e))

@router.get("/reverse", response_model=ReverseResponse)
async def reverse_geocode(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude")
):
    """
    Convert geographic coordinates into a human-readable address.
    """
    try:
        result = await GeocodingService.reverse_geocode(lat, lon)
        if not result:
            raise HTTPException(status_code=404, detail=f"No address found for coordinates ({lat}, {lon})")
        return result
    except ValueError as e:
        raise HTTPException(status_code=502, detail=str(e))
