from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status, Response

from app.models.user import User, UserRole
from app.models.organization import Organization
from app.schemas.organization import OrgRequestModel , OrgResponseModel, JoinOrgRequestModel, DelOrgResponseModel, RemoveUserFromOrgRequestModel, JoinOrgResponseModel, RemoveUserFromOrgResponseModel
from app.config.settings import settings
from app.models.api_endpoint import ApiEndpoints
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
        api = await db.execute(select(ApiEndpoints).where(ApiEndpoints.org_id==org.id))
        apis = api.scalars().all()
        for a in apis:
            await db.delete(a)
        await db.delete(org)
        await db.commit()
        return DelOrgResponseModel(
            message="Organization deleted successfully",
            org_name = org.name,
            deleted_by = user.email
            )
    @staticmethod
    async def join_org(data:JoinOrgRequestModel ,user : User, db:AsyncSession):
        if user.org_id is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User already belongs to an organization")
        result = await db.execute(select(Organization).where(Organization.id==data.organization_id))
        org = result.scalar_one_or_none()
        if not org:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Organization not found")
        user.org_id = org.id
        user.role = UserRole.viewer
        await db.commit()
        return JoinOrgResponseModel(
            message="Joined organization successfully",
            org_id=org.id,
            org_name=org.name
        )
    @staticmethod
    async def leave_org(user : User, db:AsyncSession):
        if user.org_id is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User does not belong to any organization")
        if user.role == UserRole.admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Admins cannot leave the organization. Please delete the organization instead.")
        user.org_id = None
        user.role = UserRole.viewer
        await db.commit()
        return {
            "message": "Left the organization successfully"
        }
    @staticmethod
    async def remove_user_from_org(data:RemoveUserFromOrgResponseModel , admin_user : User, db:AsyncSession):
        if admin_user.role != UserRole.admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Only admins can remove users from the organization")
        result = await db.execute(select(User).where(User.id==data.user_id , User.org_id==admin_user.org_id))
        user_to_remove = result.scalar_one_or_none()
        if not user_to_remove:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found in the organization")
        user_to_remove.org_id = None
        user_to_remove.role = UserRole.viewer
        await db.commit()
        return RemoveUserFromOrgRequestModel(
            message="User removed from organization successfully",
            user_email=user_to_remove.email,
            admin_email=admin_user.email
        )