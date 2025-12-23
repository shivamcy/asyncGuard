from pydantic import BaseModel
class UserRoleUpdateModel(BaseModel):
    new_role: str
class UserResponseModel(BaseModel):
    id: int
    email: str
    role: str
    org_id: int | None
    class Config:
        from_attributes = True