from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.config.db import get_db
from app.models.user import User , UserRole
from app.helpers.jwt import decode_access_token
from app.config.settings import settings

async def get_current_user(request : Request , db :AsyncSession =Depends(get_db))->User:
    token = request.cookies.get(settings.COOKIE_NAME)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not authenticated")
    payload=decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid or expired token")
    email = payload.get("sub")
    if not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token payload")
    result = await db.execute(select(User).where(User.email==email))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="User not found")
    request.state.user = user
    return user


def require_roles(*allowed_roles: UserRole):
    async def role_checker(
        user: User = Depends(get_current_user),
    ) -> User:
        if user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return user

    return role_checker
    
    