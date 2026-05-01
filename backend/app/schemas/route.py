"""
Pydantic schemas for Route and Optimization.
"""
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field


class LocationInput(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    address: Optional[str] = "Unknown Location"


class RouteCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    locations: List[LocationInput] = Field(..., min_length=2)


class RouteStopResponse(BaseModel):
    id: UUID
    sequence: int
    latitude: float
    longitude: float
    address: str
    status: str

    model_config = {"from_attributes": True}


class RouteResponse(BaseModel):
    route_id: UUID
    name: str
    status: str
    distance: float
    duration: float
    stops: List[RouteStopResponse]

    model_config = {"from_attributes": True}


class RouteListResponse(BaseModel):
    id: UUID
    name: str
    status: str
    stop_count: int
    created_at: datetime

    model_config = {"from_attributes": True}


class OptimizeRequest(BaseModel):
    locations: List[LocationInput] = Field(..., min_length=2)


class OptimizeResponse(BaseModel):
    route_id: Optional[UUID] = None
    distance: float
    duration: float
    geometry: List[List[float]] = []
    stops: List[dict]
