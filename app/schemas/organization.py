from pydantic import BaseModel
class OrgRequestModel(BaseModel):
    name: str
class OrgResponseModel(BaseModel):
    id:int
    name:str
class DelOrgResponseModel(BaseModel):
    message:str
    org_name:str
    deleted_by:str
    class Config:
        from_attributes = True
class JoinOrgRequestModel(BaseModel):
    organization_id: int
class RemoveUserFromOrgResponseModel(BaseModel):
    message: str
    user_email: str
    admin_email: str
class JoinOrgResponseModel(BaseModel):
    message: str
    org_id: int
    org_name: str
class RemoveUserFromOrgRequestModel(BaseModel):
    user_id: int
