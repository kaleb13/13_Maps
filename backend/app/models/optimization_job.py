"""
OptimizationJob ORM model — tracks async OSRM optimization tasks.
Updated to reference Route (not RouteRequest).
"""
import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, ForeignKey, JSON, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class OptimizationJob(Base):
    __tablename__ = "optimization_jobs"

    id          = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id      = Column(UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    owner_id    = Column(UUID(as_uuid=True), ForeignKey("users.id",         ondelete="CASCADE"), nullable=False)
    route_id    = Column(UUID(as_uuid=True), ForeignKey("routes.id",        ondelete="SET NULL"), nullable=True)

    status          = Column(String(50), default="queued",     nullable=False)  # queued | running | completed | failed
    algorithm       = Column(String(100), default="osrm_trip", nullable=False)
    profile         = Column(String(50),  default="driving",   nullable=False)
    total_distance_m= Column(Float, nullable=True)
    total_duration_s= Column(Float, nullable=True)
    result          = Column(JSON, nullable=True)
    error_message   = Column(Text, nullable=True)

    created_at   = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    def __repr__(self) -> str:
        return f"<OptimizationJob status={self.status!r}>"
