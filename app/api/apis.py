from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.db import get_db
from app.services.api_service import ApiService
from app.middleware.auth import get_current_user
from app.schemas.api import apiRequestModel , apiResponseModel
from app.models.user import User


router = APIRouter(prefix="/apis", tags=["APIs"])

@router.post("/create", response_model=apiResponseModel,status_code=status.HTTP_201_CREATED)
async def create_api(data:apiRequestModel, db:AsyncSession=Depends(get_db), user : User =Depends(get_current_user)):
    return await ApiService.create_api(data,user,db)

@router.delete("/delete/{api_id}", status_code=status.HTTP_200_OK)
async def delete_api(api_id:int, db:AsyncSession=Depends(get_db), user : User =Depends(get_current_user)):
    return await ApiService.delete_api(api_id,user,db)

@router.get("/list", response_model=list[apiResponseModel])
async def list_apis(db:AsyncSession=Depends(get_db), user : User =Depends(get_current_user)):
    return await ApiService.list_apis(db, user)

