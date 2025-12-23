from pydantic import BaseModel
from app.models.user import User, UserRole
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.schemas.user import UserRoleUpdateModel, UserResponseModel
from app.helpers.user import verify_role
class UserService:
    @staticmethod
    async def upgrade_user_role(user_id: int, data: UserRoleUpdateModel, current_user: User, db: AsyncSession) -> UserResponseModel:
        if current_user.role != UserRole.admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can upgrade user roles")
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalars().first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        verify_role(data.new_role)
        user.role = data.new_role
        await db.commit()
        await db.refresh(user)
        return UserResponseModel(
            id=user.id,
            email=user.email,
            role=user.role,
            org_id=user.org_id
        )
    