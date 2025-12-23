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
class OrgJoinRequestModel(BaseModel):
    organization_id: int
