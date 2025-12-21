from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from app.models.user import User, UserRole
from app.schemas.auth import SignupRequest, SignupResponse, LoginRequest, LoginResponse
from app.helpers.jwt import create_access_token
from app.helpers.hashing import verify_password
from app.helpers.hashing import hash_password

class AuthService:
    @staticmethod
    async def signup(data:SignupRequest , db :AsyncSession)->SignupResponse:
        result = await db.execute(select(User).where(User.email==data.email))
        if result.scalar_one_or_none():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="user already exists")
        hashed_pass=hash_password(data.password)
        user = User(
            email=data.email,
            hashed_password=hashed_pass,
            role=UserRole.viewer,
            org_id=None
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return SignupResponse(
            id=user.id,
            email=user.email,
            role=user.role.value,
            org_id=user.org_id
            
        )
    @staticmethod
    async def login(data:LoginRequest , db :AsyncSession)->LoginResponse:
        result = await db.execute(select(User).where(User.email==data.email))
        user = result.scalar_one_or_none()
        if not user or not verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        
        access_token = create_access_token(data={"sub": user.email, "user_id": user.id, "role": user.role.value})
        
        return LoginResponse(
            access_token=access_token,
            user_id=user.id,
            email=user.email,
            role=user.role.value,
            org_id=user.org_id
        )
        