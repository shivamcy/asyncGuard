from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.audit_run import AuditRun
from app.models.api_endpoint import ApiEndpoints
from app.audit.runner import AuditRunner

class AuditService:
    @staticmethod
    async def run_audit(api_id: int, db: AsyncSession):
        api = await db.get(ApiEndpoints, api_id)
        if not api:
            raise ValueError("API not found")

        now = datetime.now(timezone.utc)

        audit_run = AuditRun(
            api_id=api.id,
            score=0,
            time_window=now,
        )

        db.add(audit_run)
        await db.commit()
        await db.refresh(audit_run)

        await AuditRunner.run(api, audit_run, db)

        return audit_run
