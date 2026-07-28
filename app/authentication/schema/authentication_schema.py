from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, List, Any


class AuthRegisterRequestSchema(BaseModel):
    name : str
    email : EmailStr
    phone : str
    password : str
    confirm_password : str
    role : int = 1

    @field_validator("confirm_password")
    @classmethod
    def password_match(cls, value,info):
        if value != info.data.get("password"):
            raise ValueError ("Password do not match")
        return value
    
    @field_validator("role")
    def role_validator(cls, value, info):
        allowed_roles = [1,3]
        if value not in allowed_roles:
            raise ValueError("Invalid role")
        return value

    
class AuthRegisterResponseSchema(BaseModel):
    id : Optional[int] = None
    name : Optional[str] = None
    email : Optional[EmailStr] = None
    phone : Optional[str] = None
    class Config:
        from_attributes = True


class AuthLoginRequestSchema(BaseModel):
    email : EmailStr
    password : str
    

class AuthLoginResponseSchema(BaseModel):
    token_type : str
    access_token : str
    refresh_token :str
        
class RefreshTokenRequestSchema(BaseModel):
    refresh_token : str
    
class RoleSchema(BaseModel):
    id: int
    name: str
    description: Optional[str] = None


class OrderSchema(BaseModel):
    id : Optional[Any] 
    user_id : Optional[Any]  
    total_amount : Optional[Any] 
    status : Optional[Any]  
    class Config:
        from_attributes = True
        
        
class AuthMeResponseSchema(BaseModel):
    id :int
    name : str
    email :EmailStr
    phone :Optional[str] = None
    roles : Optional[List[RoleSchema]] = []
    carts : Optional[list[Any]] = []
    orders : Optional[list[Any]] = []
    class Config:
        from_attributes = True


class AuthUpdatePassRequestSchema(BaseModel):
    current_password : str
    new_password : str
    confirm_password : str 
    
class ForgotPasswordRequestSchema(BaseModel):
    email : EmailStr
    
class ResetPasswordRequestSchema(BaseModel):
    password : str
    confirm_pass : str