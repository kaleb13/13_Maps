"""
Pydantic schemas for OptimizationJob domain.
"""
from typing import List, Optional, Any
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field


class OptimizeRequest(BaseModel):
    route_request_id: UUID
    profile: str = Field("driving", pattern="^(driving|cycling|walking)$")
    algorithm: str = Field("osrm_trip", pattern="^(osrm_trip|osrm_route)$")


class OptimizationJobRead(BaseModel):
    id: UUID
    owner_id: UUID
    route_id: Optional[UUID]
    status: str
    algorithm: str
    profile: str
    total_distance_m: Optional[float]
    total_duration_s: Optional[float]
    result: Optional[Any]
    error_message: Optional[str]
    created_at: datetime
    completed_at: Optional[datetime]

    model_config = {"from_attributes": True}
