from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.audit_run import AuditRun
from app.models.api_endpoint import ApiEndpoints
from app.audit.runner import AuditRunner
from app.models.user import User
from app.models.user import UserRole
from fastapi import HTTPException, status

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
    # @staticmethod
    # async def get_audit_results(api_id: int, user: User, db: AsyncSession):
    #     api = await db.get(ApiEndpoints, api_id)
    #     if not api:
    #         raise HTTPException(
    #             detail = "API not found",
    #             status_code=status.HTTP_404_NOT_FOUND
    #         )

    #     results = await db.execute(
    #         select(AuditRun).where(AuditRun.api_id == api_id).order_by(AuditRun.time_window.desc())
    #     )
    #     audits = results.scalars().all()

    #     return {
    #         "api_id": api_id,"latest_audits": audits[0] if audits else None
    #     }
    
    # @staticmethod
    # async def get_all_latest_audit_results(user: User, db: AsyncSession):
    #     if user.org_id is None:
    #         raise HTTPException(
    #             status_code=status.HTTP_400_BAD_REQUEST,
    #             detail="User does not belong to any organization"
    #         )

    #     apis = (
    #         await db.execute(
    #             select(ApiEndpoints).where(ApiEndpoints.org_id == user.org_id)
    #         )
    #     ).scalars().all()

    #     response = []

    #     for api in apis:
    #         audit = (
    #             await db.execute(
    #                 select(AuditRun)
    #                 .where(AuditRun.api_id == api.id)
    #                 .order_by(AuditRun.time_window.desc())
    #                 .limit(1)
    #             )
    #         ).scalar_one_or_none()

    #         response.append({
    #             "api": {
    #                 "id": api.id,
    #                 "name": api.name,
    #                 "url": api.url
    #             },
    #             "latest_audit": audit
    #         })

    #     return response

