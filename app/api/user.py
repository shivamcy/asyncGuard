from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.db import get_db
from app.models.user import User
from app.middleware.auth import get_current_user
from app.services.user_service import UserService
from app.schemas.user import UserRoleUpdateModel, UserResponseModel


router = APIRouter(prefix="/user", tags=["users"])

@router.patch("upgrade/{user_id}", response_model=UserResponseModel, status_code=status.HTTP_200_OK)
async def upgrade_user_role(user_id : int, data: UserRoleUpdateModel, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await UserService.upgrade_user_role(user_id, data, current_user, db)