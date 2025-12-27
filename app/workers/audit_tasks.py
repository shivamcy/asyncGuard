import asyncio
from sqlalchemy import select

from app.config.celery import celery_app
from app.config.db import AsyncSessionLocal
from app.services.audit_service import AuditService
from app.models.api_endpoint import ApiEndpoints
from app.models.dead_letter import DeadLetterTask


@celery_app.task(bind=True, max_retries=3, default_retry_delay=10)
def run_audit_task(self, api_id: int):
    try:
        asyncio.run(_run_single(api_id))
    except Exception as exc:
        if self.request.retries >= self.max_retries:
            asyncio.run(_send_to_dlq(api_id, exc, self.request.retries))
        raise self.retry(exc=exc)


async def _run_single(api_id: int):
    async with AsyncSessionLocal() as db:
        await AuditService.run_audit(api_id, db)


@celery_app.task
def run_all_audits():
    asyncio.run(_run_all())


async def _run_all():
    async with AsyncSessionLocal() as db:
        apis = (await db.execute(select(ApiEndpoints))).scalars().all()
        for api in apis:
            run_audit_task.delay(api.id)


async def _send_to_dlq(api_id: int, exc: Exception, retries: int):
    async with AsyncSessionLocal() as db:
        db.add(
            DeadLetterTask(
                task_name="run_audit_task",
                payload=str({"api_id": api_id}),
                error=str(exc),
                retry_count=retries,
            )
        )
        await db.commit()
