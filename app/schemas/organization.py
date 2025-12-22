from pydantic import BaseModel
class OrgRequestModel(BaseModel):
    name: str
class OrgResponseModel(BaseModel):
    id:int
    name:str
    class Config:
        from_attributes = True
