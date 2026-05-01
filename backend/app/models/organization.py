"""
Organization ORM model — multi-tenant root entity.
Every resource (users, vehicles, jobs, routes) belongs to one organization.
"""
import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(200), nullable=False)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    plan = Column(String(50), default="free", nullable=False)          # free | pro | enterprise
    address = Column(Text, nullable=True)
    phone = Column(String(30), nullable=True)
    email = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    users    = relationship("User",    back_populates="organization", lazy="selectin")
    vehicles = relationship("Vehicle", back_populates="organization", lazy="selectin")
    jobs     = relationship("Job",     back_populates="organization", lazy="selectin")
    routes   = relationship("Route",   back_populates="organization", lazy="selectin")

    def __repr__(self) -> str:
        return f"<Organization {self.slug!r}>"
