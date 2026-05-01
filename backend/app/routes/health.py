"""
Health check endpoints — no auth required.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
import httpx

from app.core.database import get_db
from app.core.config import settings

router = APIRouter()


@router.get("/health", summary="API health check")
async def health_check():
    return {
        "status": "ok",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }


@router.get("/health/db", summary="Database health check")
async def db_health(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "error", "database": str(e)}


@router.get("/health/osrm", summary="OSRM engine health check")
async def osrm_health():
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            # OSRM nearest endpoint as a lightweight probe
            resp = await client.get(
                f"{settings.OSRM_BASE_URL}/nearest/v1/driving/0,0"
            )
        return {"status": "ok", "osrm": resp.status_code}
    except Exception as e:
        return {"status": "error", "osrm": str(e)}
