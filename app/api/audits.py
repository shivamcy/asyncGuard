from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.limiter import user_limiter
from app.middleware.auth import get_current_user
from app.models.user import User
from app.config.db import get_db
from app.helpers.authorization import validate_user , validate_api_belongs_to_user_org

router = APIRouter(prefix="/audits", tags=["Audits"])

@router.post("/run/{api_id}", status_code=status.HTTP_202_ACCEPTED)
@user_limiter.limit("5/minute")
async def run_audit(api_id: int, user: User = Depends(get_current_user),db: AsyncSession = Depends(get_db)):
    await validate_user(user)
    await validate_api_belongs_to_user_org(api_id,user,db)

