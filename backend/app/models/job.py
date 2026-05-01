"""
Job ORM model — a delivery point / task to be included in a route.
Each job represents one stop with geo-coordinates, time windows,
and capacity requirements.
"""
import uuid
from datetime import datetime, timezone

import sqlalchemy as sa
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text, Time
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base

# ── Enums ─────────────────────────────────────────────────────────────────────
JobStatus = sa.Enum(
    "pending",    # not yet assigned to a route
    "assigned",   # assigned to a route but not dispatched
    "in_transit", # driver is en route to this stop
    "completed",  # delivered successfully
    "failed",     # delivery attempted but failed
    "cancelled",  # job cancelled
    name="job_status",
    create_type=True,
)

JobPriority = sa.Enum(
    "low", "normal", "high", "urgent",
    name="job_priority",
    create_type=True,
)


class Job(Base):
    __tablename__ = "jobs"

    id           = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id       = Column(UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)

    # ── Identity ──────────────────────────────────────────────────────────────
    title        = Column(String(255), nullable=False)
    reference    = Column(String(100), nullable=True, index=True)  # external order/waybill number

    # ── Location ──────────────────────────────────────────────────────────────
    address      = Column(Text,    nullable=False)
    latitude     = Column(Float,   nullable=False)
    longitude    = Column(Float,   nullable=False)
    city         = Column(String(100), nullable=True)
    postal_code  = Column(String(20),  nullable=True)

    # ── Contact ───────────────────────────────────────────────────────────────
    contact_name  = Column(String(150), nullable=True)
    contact_phone = Column(String(30),  nullable=True)
    contact_email = Column(String(255), nullable=True)

    # ── Scheduling ────────────────────────────────────────────────────────────
    scheduled_date     = Column(sa.Date, nullable=True)
    time_window_start  = Column(Time,    nullable=True)   # earliest arrival
    time_window_end    = Column(Time,    nullable=True)   # latest arrival
    service_time_min   = Column(Integer, default=10, nullable=False)  # stop dwell time in minutes

    # ── Capacity ──────────────────────────────────────────────────────────────
    weight_kg    = Column(Float, default=0.0, nullable=False)
    volume_m3    = Column(Float, default=0.0, nullable=False)
    quantity     = Column(Integer, default=1, nullable=False)

    # ── Status & Priority ─────────────────────────────────────────────────────
    status       = Column(JobStatus,   nullable=False, default="pending",  server_default="pending")
    priority     = Column(JobPriority, nullable=False, default="normal",   server_default="normal")

    notes        = Column(Text, nullable=True)
    created_at   = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at   = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    organization  = relationship("Organization", back_populates="jobs")
    route_stops   = relationship("RouteStop", back_populates="job")

    def __repr__(self) -> str:
        return f"<Job {self.title!r} status={self.status!r}>"
