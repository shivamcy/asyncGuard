from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User , UserRole
from app.models.api_endpoint import ApiEndpoints
async def validate_user(user :User):
    if user.role.value == UserRole.viewer:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Admin/Auditer privileges required")
async def validate_api_belongs_to_user_org(api_id:int , user: User ,db:AsyncSession) ->ApiEndpoints:
    api = await db.get(ApiEndpoints,api_id)
    if not api:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="API not found")
    if api.org_id!=user.org_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="API does not belong to your organization")
    return api