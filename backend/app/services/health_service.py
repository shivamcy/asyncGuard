from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from fastapi import HTTPException, status
import redis.asyncio as redis

from app.config.settings import settings


class HealthService:

    @staticmethod
    async def db_health(db: AsyncSession):
        try:
            await db.execute(text("SELECT 1"))
            return {"db": "ok"}
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database unavailable",
            )

    @staticmethod
    async def redis_health():
        try:
            r = redis.from_url(settings.REDIS_URL)
            await r.ping()
            return {"redis": "ok"}
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Redis unavailable",
            )

    @staticmethod
    async def full_health(db: AsyncSession):
        health = {
            "app": "ok",
            "db": "ok",
            "redis": "ok",
        }

        try:
            await db.execute(text("SELECT 1"))
        except Exception:
            health["db"] = "down"

        try:
            r = redis.from_url(settings.REDIS_URL)
            await r.ping()
        except Exception:
            health["redis"] = "down"

        if "down" in health.values():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=health,
            )

        return health
