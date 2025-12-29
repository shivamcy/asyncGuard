from fastapi import APIRouter, Depends, Response, status, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.db import get_db
from app.schemas.auth import SignupRequest, SignupResponse, LoginRequest
from app.services.auth_service import AuthService
from app.config.limiter import limiter
from app.models.user import User
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup", response_model=SignupResponse)
@limiter.limit("5/minute")
async def signup(request: Request, data: SignupRequest, db: AsyncSession = Depends(get_db)):
    return await AuthService.signup(data, db)


@router.post("/login", status_code=status.HTTP_200_OK)
@limiter.limit("5/minute")
async def login(request: Request, data: LoginRequest, response: Response, db: AsyncSession = Depends(get_db)):
    return await AuthService.login(data, response, db)

@router.get("/me", status_code=status.HTTP_200_OK)
async def me(user: User = Depends(get_current_user)):
    return await AuthService.me(user)

@router.post("/logout", status_code=status.HTTP_200_OK)
@limiter.limit("5/minute")
async def logout(request: Request, response: Response):
    return await AuthService.logout(response)
