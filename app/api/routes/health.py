import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.core.database import check_database_health, get_database

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/")
async def health_check():
    """Basic health check endpoint."""
    return {
        "status": "healthy",
        "version": settings.app_version,
        "environment": settings.environment,
    }


@router.get("/ready")
async def readiness_check(db: AsyncSession | None = Depends(get_database)):
    """Readiness check endpoint that includes database connectivity."""
    db_status = await check_database_health()

    if not db_status:
        raise HTTPException(status_code=503, detail="Database is not available")

    return {
        "status": "ready",
        "version": settings.app_version,
        "environment": settings.environment,
        "database": "connected" if settings.database_url else "not configured",
    }
