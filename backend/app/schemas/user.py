"""
Pydantic schemas for User domain.
"""
from typing import Optional
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    full_name: Optional[str] = Field(None, max_length=150)
    org_name: Optional[str] = Field(None, description="Only for registration")

class UserCreateInternal(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    full_name: Optional[str] = Field(None, max_length=150)
    role: str = Field("driver", pattern="^(admin|manager|driver)$")
    org_id: UUID

class UserRead(BaseModel):
    id: UUID
    org_id: UUID
    email: EmailStr
    full_name: Optional[str]
    role: str
    is_active: bool
    is_superuser: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, max_length=150)
    password: Optional[str] = Field(None, min_length=8, max_length=128)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
