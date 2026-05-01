"""
User ORM model — expanded with roles and organization membership.
"""
import uuid
from datetime import datetime, timezone

import sqlalchemy as sa
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base

# ── Role enum ────────────────────────────────────────────────────────────────
UserRole = sa.Enum(
    "admin",    # full access within the org
    "manager",  # can manage routes, jobs, vehicles; cannot manage users
    "driver",   # read-only dashboard + own assigned routes
    name="user_role",
    create_type=True,
)


class User(Base):
    __tablename__ = "users"

    id              = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id          = Column(UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    email           = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    full_name       = Column(String(150), nullable=True)
    role            = Column(UserRole, nullable=False, default="driver", server_default="driver")
    phone           = Column(String(30), nullable=True)
    avatar_url      = Column(String(500), nullable=True)
    is_active       = Column(Boolean, default=True, nullable=False)
    is_superuser    = Column(Boolean, default=False, nullable=False)   # platform-level admin
    last_login_at   = Column(DateTime(timezone=True), nullable=True)
    created_at      = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at      = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    organization     = relationship("Organization", back_populates="users")
    driven_vehicles  = relationship("Vehicle", back_populates="driver",       foreign_keys="Vehicle.driver_id")
    driven_routes    = relationship("Route",   back_populates="driver",        foreign_keys="Route.driver_id")
    managed_routes   = relationship("Route",   back_populates="created_by",    foreign_keys="Route.created_by_id")

    def __repr__(self) -> str:
        return f"<User {self.email!r} role={self.role!r}>"
