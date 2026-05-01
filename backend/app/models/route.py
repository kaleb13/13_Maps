"""
Route and RouteStop ORM models — optimized route results.

Route       → the plan for one vehicle's run (header)
RouteStop   → ordered stops within that route (junction to Job)
"""
import uuid
from datetime import datetime, timezone

import sqlalchemy as sa
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base

# ── Enums ─────────────────────────────────────────────────────────────────────
RouteStatus = sa.Enum(
    "draft",       # not yet dispatched
    "optimized",   # OSRM result available
    "dispatched",  # sent to driver
    "in_progress", # driver has started
    "completed",   # all stops done
    "cancelled",
    name="route_status",
    create_type=True,
)

StopStatus = sa.Enum(
    "pending",
    "arrived",
    "completed",
    "skipped",
    name="stop_status",
    create_type=True,
)


class Route(Base):
    __tablename__ = "routes"

    id             = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id         = Column(UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    vehicle_id     = Column(UUID(as_uuid=True), ForeignKey("vehicles.id",      ondelete="SET NULL"),  nullable=True,  index=True)
    driver_id      = Column(UUID(as_uuid=True), ForeignKey("users.id",         ondelete="SET NULL"),  nullable=True,  index=True)
    created_by_id  = Column(UUID(as_uuid=True), ForeignKey("users.id",         ondelete="SET NULL"),  nullable=True)

    # ── Identity ──────────────────────────────────────────────────────────────
    name           = Column(String(255), nullable=False)
    status         = Column(RouteStatus, nullable=False, default="draft", server_default="draft")

    # ── Optimization settings ─────────────────────────────────────────────────
    profile        = Column(String(50),  default="driving",   nullable=False)   # driving | cycling | walking
    algorithm      = Column(String(100), default="osrm_trip", nullable=False)   # osrm_trip | osrm_route

    # ── Scheduling ────────────────────────────────────────────────────────────
    scheduled_date  = Column(sa.Date, nullable=True)
    departure_time  = Column(sa.Time, nullable=True)

    # ── Results (filled after optimization) ───────────────────────────────────
    total_distance_m  = Column(Float,   nullable=True)
    total_duration_s  = Column(Float,   nullable=True)
    total_weight_kg   = Column(Float,   nullable=True)
    total_volume_m3   = Column(Float,   nullable=True)
    stop_count        = Column(Integer, nullable=True)
    osrm_response     = Column(JSON,    nullable=True)   # raw OSRM payload

    notes          = Column(Text,    nullable=True)
    completed_at   = Column(DateTime(timezone=True), nullable=True)
    created_at     = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at     = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    organization = relationship("Organization", back_populates="routes")
    vehicle      = relationship("Vehicle",      back_populates="routes",      foreign_keys=[vehicle_id])
    driver       = relationship("User",         back_populates="driven_routes", foreign_keys=[driver_id])
    created_by   = relationship("User",         back_populates="managed_routes", foreign_keys=[created_by_id])
    stops        = relationship("RouteStop",    back_populates="route",
                                cascade="all, delete-orphan",
                                order_by="RouteStop.sequence")

    def __repr__(self) -> str:
        return f"<Route {self.name!r} status={self.status!r}>"


class RouteStop(Base):
    """Ordered stop within a Route, referencing a Job."""
    __tablename__ = "route_stops"

    id         = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    route_id   = Column(UUID(as_uuid=True), ForeignKey("routes.id", ondelete="CASCADE"), nullable=False, index=True)
    job_id     = Column(UUID(as_uuid=True), ForeignKey("jobs.id",   ondelete="RESTRICT"), nullable=False, index=True)

    sequence         = Column(Integer, nullable=False)            # 1-based order in route
    estimated_arrival= Column(sa.Time, nullable=True)
    actual_arrival   = Column(DateTime(timezone=True), nullable=True)
    actual_departure = Column(DateTime(timezone=True), nullable=True)
    status           = Column(StopStatus, nullable=False, default="pending", server_default="pending")
    driver_notes     = Column(Text, nullable=True)

    # Relationships
    route = relationship("Route", back_populates="stops")
    job   = relationship("Job",   back_populates="route_stops")

    def __repr__(self) -> str:
        return f"<RouteStop seq={self.sequence} job={self.job_id}>"
