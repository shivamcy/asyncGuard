from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.middleware.auth import get_current_user
from app.models.user import User
from app.config.db import get_db
from app.services.report_service import ReportService
from app.config.limiter import user_limiter
router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/results/{api_id}", status_code=status.HTTP_200_OK)
@user_limiter.limit("5/minute")
async def get_audit_results(api_id: int, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    return await ReportService.get_audit_results(api_id, user, db)

@router.get("/results", status_code=status.HTTP_200_OK)
@user_limiter.limit("5/minute")
async def get_all_audit_results(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    return await ReportService.get_all_audit_results(user, db)