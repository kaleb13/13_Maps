"""
User service — business logic for user management.
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from app.models.user import User
from app.core.security import hash_password


async def get_user_by_id(db: AsyncSession, user_id: str) -> User:
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def deactivate_user(db: AsyncSession, user_id: str) -> User:
    user = await get_user_by_id(db, user_id)
    user.is_active = False
    await db.flush()
    return user


async def update_password(db: AsyncSession, user_id: str, new_password: str) -> None:
    user = await get_user_by_id(db, user_id)
    user.hashed_password = hash_password(new_password)
    await db.flush()
