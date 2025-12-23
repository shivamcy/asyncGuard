from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.db import get_db
from app.schemas.organization import OrgRequestModel , OrgResponseModel, JoinOrgRequestModel, DelOrgResponseModel, JoinOrgResponseModel, RemoveUserFromOrgResponseModel, RemoveUserFromOrgRequestModel
from app.services.org_service import OrgService
from app.middleware.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/organizations", tags=["Organization"])

@router.post("/create",response_model=OrgResponseModel,status_code=status.HTTP_201_CREATED)
async def create_org(data:OrgRequestModel, db:AsyncSession=Depends(get_db), user : User =Depends(get_current_user)):
    return await OrgService.create_org(data,user,db)


@router.delete("/delete", response_model=DelOrgResponseModel , status_code=status.HTTP_200_OK)
async def delete_org(db:AsyncSession=Depends(get_db), user : User =Depends(get_current_user)):
    return await OrgService.delete_org(user,db)

@router.post("/join", response_model=JoinOrgResponseModel, status_code=status.HTTP_200_OK)
async def join_org(data:JoinOrgRequestModel, db:AsyncSession=Depends(get_db), user : User =Depends(get_current_user)):
    return await OrgService.join_org(data,user,db)

@router.post("/leave", status_code=status.HTTP_200_OK)
async def leave_org( db:AsyncSession=Depends(get_db), user : User =Depends(get_current_user)):
    return await OrgService.leave_org(user,db)  

@router.post("/remove_user", response_model=RemoveUserFromOrgResponseModel , status_code=status.HTTP_200_OK)
async def remove_user_from_org(data:RemoveUserFromOrgRequestModel, db:AsyncSession=Depends(get_db), user : User =Depends(get_current_user)):
    return await OrgService.remove_user_from_org(data,user,db)