"""
Vehicle ORM model — fleet management with capacity constraints.
"""
import uuid
from datetime import datetime, timezone

import sqlalchemy as sa
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base

# ── Enums ─────────────────────────────────────────────────────────────────────
VehicleType = sa.Enum(
    "car", "van", "truck", "motorcycle", "bicycle",
    name="vehicle_type",
    create_type=True,
)

VehicleStatus = sa.Enum(
    "available", "on_route", "maintenance", "retired",
    name="vehicle_status",
    create_type=True,
)


class Vehicle(Base):
    __tablename__ = "vehicles"

    id                 = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id             = Column(UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    driver_id          = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)

    name               = Column(String(150), nullable=False)
    license_plate      = Column(String(30),  nullable=True, index=True)
    vehicle_type       = Column(VehicleType, nullable=False, default="van", server_default="van")
    status             = Column(VehicleStatus, nullable=False, default="available", server_default="available")

    # Capacity
    capacity_weight_kg = Column(Float, nullable=True)   # max payload weight
    capacity_volume_m3 = Column(Float, nullable=True)   # max payload volume
    max_stops          = Column(sa.Integer, nullable=True)  # max delivery stops per route

    # Operational
    fuel_type          = Column(String(50), nullable=True)  # diesel | petrol | electric | hybrid
    speed_profile      = Column(String(50), default="driving", nullable=False)  # driving | cycling
    notes              = Column(Text, nullable=True)
    is_active          = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    organization = relationship("Organization", back_populates="vehicles")
    driver       = relationship("User",         back_populates="driven_vehicles", foreign_keys=[driver_id])
    routes       = relationship("Route",        back_populates="vehicle")

    def __repr__(self) -> str:
        return f"<Vehicle {self.name!r} [{self.license_plate}]>"
