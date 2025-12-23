from pydantic import BaseModel
from datetime import datetime
class ApiRequestModel(BaseModel):
    name: str
    #description: str
    url: str
class ApiResponseModel(BaseModel):
    id: int
    name: str
    #description: str
    org_id: int
    url: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
class DeleteApiResponseModel(BaseModel):
    message: str
    api_name: str
    api_url: str
    deleted_by: str


#discuss : should we add description field here?