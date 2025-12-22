from pydantic import BaseModel
from datetime import datetime
class apiRequestModel(BaseModel):
    name: str
    #description: str
    url: str
class apiResponseModel(BaseModel):
    id: int
    name: str
    #description: str
    org_id: int
    url: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


#discuss : should we add description field here?