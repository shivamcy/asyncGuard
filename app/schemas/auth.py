from pydantic import BaseModel, EmailStr
class SignupRequest(BaseModel):
    email:EmailStr
    password:str
class SignupResponse(BaseModel):
    id:int
    email:EmailStr
    role:str
    org_id: int| None
class LoginRequest(BaseModel):
    email:EmailStr
    password:str
class LoginResponse(BaseModel):
    access_token:str
    token_type:str = "bearer"
    user_id:int
    email:EmailStr
    role:str
    org_id: int| None