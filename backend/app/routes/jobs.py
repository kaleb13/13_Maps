"""
Jobs endpoints — poll optimization job status.
"""
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.permissions import require_roles
from app.models.user import User
from app.models.optimization_job import OptimizationJob
from app.schemas.optimization import OptimizationJobRead

router = APIRouter()


@router.get("/", response_model=List[OptimizationJobRead])
async def list_jobs(
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(["admin", "manager", "driver"])),
):
    result = await db.execute(
        select(OptimizationJob)
        .where(OptimizationJob.org_id == current_user.org_id)
        .order_by(OptimizationJob.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


@router.get("/{job_id}", response_model=OptimizationJobRead)
async def get_job(
    job_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(["admin", "manager", "driver"])),
):
    result = await db.execute(
        select(OptimizationJob).where(
            OptimizationJob.id == job_id,
            OptimizationJob.org_id == current_user.org_id,
        )
    )
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job
