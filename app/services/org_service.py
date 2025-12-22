from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status, Response

from app.models.user import User, UserRole
from app.models.organization import Organization
from app.schemas.organization import OrgRequestModel , OrgResponseModel
from app.config.settings import settings
class OrgService:
    @staticmethod
    async def create_org(data : OrgRequestModel ,user : User, db:AsyncSession)->OrgResponseModel:
        if user.org_id is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User already belongs to an organization")
        if user.role != UserRole.viewer:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="only viewers can create  an organization")
        result = await db.execute(select(Organization).where(Organization.name==data.name))
        existing_org = result.scalar_one_or_none()
        if existing_org :
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Organization already exists")
        org=Organization(
            name=data.name
        )
        db.add(org)
        await db.flush() 
        user.org_id = org.id
        user.role = UserRole.admin

        await db.commit()
        await db.refresh(org)

        return OrgResponseModel(
            id=org.id,
            name=org.name,
        )
    @staticmethod
    async def delete_org(user : User, db:AsyncSession):
        if user.org_id is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User does not belong to any organization")
        if user.role != UserRole.admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Only admins can delete the organization")
        result = await db.execute(select(Organization).where(Organization.id==user.org_id))
        org = result.scalar_one_or_none()
        if not org:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Organization not found")
        users_in_org = await db.execute(select(User).where(User.org_id==org.id))
        users = users_in_org.scalars().all()
        for u in users:
            u.org_id = None
            u.role = UserRole.viewer
        await db.delete(org)
        await db.commit()
        return {
            "detail":"Organization deleted successfully",
            "org_name" : org.name,
            "deleted_by" : user.email
            }