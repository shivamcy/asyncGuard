from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.middleware.auth import get_current_user
from app.models.user import User
from app.workers.audit_tasks import run_audit_task

router = APIRouter(prefix="/audits", tags=["Audits"])

@router.post("/run/{api_id}", status_code=status.HTTP_202_ACCEPTED)
async def run_audit(api_id: int, user: User = Depends(get_current_user)):
    if user.role.value != "admin":
        raise PermissionError("Only admins can run audits")

    run_audit_task.delay(api_id)
    return {"message": "Audit scheduled"}
