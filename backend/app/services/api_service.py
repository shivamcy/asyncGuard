from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select , desc
from fastapi import HTTPException, status, Response

from app.schemas.api import ApiRequestModel, ApiResponseModel, DeleteApiResponseModel
from app.models.user import User, UserRole
from app.models.api_endpoint import ApiEndpoints
from app.models.audit_run import AuditRun
from app.models.audit_result import AuditResult

class ApiService:
    @staticmethod
    async def create_api(data: ApiRequestModel, user: User, db: AsyncSession) -> ApiResponseModel:
        if user.org_id is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User does not belong to any organization")
        if user.role != UserRole.admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can create APIs")
        if api := await db.execute(select(ApiEndpoints).where(ApiEndpoints.name == data.name, ApiEndpoints.org_id == user.org_id)):
            existing_api = api.scalar_one_or_none()
            if existing_api:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="API with this name already exists in the organization")
        if api_url := await db.execute(select(ApiEndpoints).where(ApiEndpoints.url == data.url, ApiEndpoints.org_id == user.org_id)):
            existing_url = api_url.scalar_one_or_none()
            if existing_url:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="API with this URL already exists in the organization")
        api = ApiEndpoints(
            name=data.name,
            url=data.url,
            org_id=user.org_id
        )
        db.add(api)
        await db.flush()
        await db.commit()
        await db.refresh(api)
        return ApiResponseModel(
            id=api.id,
            name=api.name,
            org_id=api.org_id,
            url=api.url,
            is_active=api.is_active,
            created_at=api.created_at
        )
    @staticmethod
    async def delete_api(api_id: int, user: User, db: AsyncSession):
        if user.org_id is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User does not belong to any organization")
        if user.role != UserRole.admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can delete APIs")
        result = await db.execute(select(ApiEndpoints).where(ApiEndpoints.id == api_id, ApiEndpoints.org_id == user.org_id))
        api = result.scalar_one_or_none()
        if not api:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="API not found")
        await db.delete(api)
        await db.commit()
        return DeleteApiResponseModel(
            message= "API deleted successfully",
            api_name= api.name,
            api_url= api.url,
            deleted_by= user.email
        )
    @staticmethod
    async def list_apis(db: AsyncSession, user: User) -> list[ApiResponseModel]:
        if user.org_id is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User does not belong to any organization")
        result = await db.execute(select(ApiEndpoints).where(ApiEndpoints.is_active==True, ApiEndpoints.org_id == user.org_id) ) 
        apis = result.scalars().all()
        return [
            ApiResponseModel(
                id=api.id,
                name=api.name,
                url=api.url,
                is_active=api.is_active,
                org_id=api.org_id,
                created_at=api.created_at
            ) for api in apis
        ]
    @staticmethod
    async def list_error(api_id: int, db: AsyncSession, user: User):

        
        api_stmt = select(ApiEndpoints).where(ApiEndpoints.id == api_id,ApiEndpoints.org_id == user.org_id)

        api = (await db.execute(api_stmt)).scalar_one_or_none()

        if not api:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="API not found or access denied")

        
        audit_run_stmt = (select(AuditRun).where(AuditRun.api_id == api_id).order_by(desc(AuditRun.created_at)).limit(1))

        audit_run = (await db.execute(audit_run_stmt)).scalar_one_or_none()

        if not audit_run:
            return {
                "api_id": api_id,
                "results": []
            }

        
        audit_results_stmt = (select(AuditResult.details).where(AuditResult.audit_run_id == audit_run.id))

        details = (await db.execute(audit_results_stmt)).scalars().all()

        return {
          "api_id": api_id,
          "results": [{"details": d} for d in details]
        }   