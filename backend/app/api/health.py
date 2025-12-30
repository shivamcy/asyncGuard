from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.db import get_db
from app.services.health_service import HealthService

router = APIRouter(prefix="/health", tags=["HEALTH"])


@router.get("")
async def health_check():
    return {"status": "ok"}


@router.get("/db")
async def db_health(db: AsyncSession = Depends(get_db)):
    return await HealthService.db_health(db)


@router.get("/redis")
async def redis_health():
    return await HealthService.redis_health()


@router.get("/full")
async def full_health(db: AsyncSession = Depends(get_db)):
    return await HealthService.full_health(db)
