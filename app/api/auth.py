from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.db import get_db
from app.schemas.auth import SignupRequest, SignupResponse, LoginRequest
from app.services.auth_service import AuthService
from app.config.limiter import ip_limiter

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup", response_model=SignupResponse)
@ip_limiter.limit("5/minute")
async def signup(data: SignupRequest, db: AsyncSession = Depends(get_db)):
    return await AuthService.signup(data, db)


@router.post("/login", status_code=status.HTTP_200_OK)
@ip_limiter.limit("5/minute")
async def login(data: LoginRequest, response: Response, db: AsyncSession = Depends(get_db)):
    return await AuthService.login(data, response, db)


@router.post("/logout", status_code=status.HTTP_200_OK)
@ip_limiter.limit("5/minute")
async def logout(response: Response):
    return await AuthService.logout(response)
