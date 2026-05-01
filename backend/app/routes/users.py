"""
Users endpoints — User management and RBAC assignment.
"""
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import hash_password
from app.core.permissions import require_roles, require_superuser
from app.models.user import User
from app.schemas.user import UserCreateInternal, UserRead

router = APIRouter()


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    payload: UserCreateInternal,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(["admin"])),
):
    """
    Create a new user. 
    Admins can create users within their own organization.
    Superusers can create users in any organization.
    """
    # Authorization checks
    if not current_user.is_superuser:
        # Regular admins can only create users in their own org
        if payload.org_id != current_user.org_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only create users within your own organization."
            )
        # Regular admins cannot create other admins or superusers (optional business logic)
        if payload.role == "admin":
             raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot create additional admin users without superuser privileges."
            )

    # Check email duplicate
    result = await db.execute(select(User).where(User.email == payload.email))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    user = User(
        org_id=payload.org_id,
        email=payload.email,
        hashed_password=hash_password(payload.password),
        full_name=payload.full_name,
        role=payload.role
    )
    db.add(user)
    await db.flush()
    await db.refresh(user)
    return user


@router.get("/", response_model=List[UserRead])
async def list_users(
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(["admin", "manager"])),
):
    """
    List users in the organization.
    """
    query = select(User)
    
    if not current_user.is_superuser:
        query = query.where(User.org_id == current_user.org_id)
        
    result = await db.execute(query.offset(skip).limit(limit))
    return result.scalars().all()


@router.get("/me", response_model=UserRead)
async def read_users_me(current_user: User = Depends(require_roles(["admin", "manager", "driver"]))):
    """
    Get current user profile.
    """
    return current_user
