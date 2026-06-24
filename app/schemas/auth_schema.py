from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, List
class RegisterRequest(BaseModel):
    name : str
    email : EmailStr
    phone : str
    password : str
    confirm_password : str
    role : str

    @field_validator("confirm_password")
    @classmethod
    def password_match(cls, value,info):
        if value != info.data.get("password"):
            raise ValueError ("Password do not match")
        return value
    
    @field_validator("role")
    def role_validator(cls, value, info):
        allowed_roles = ["CUSTOMER", "CANTEEN_OWNER"]
        if value not in allowed_roles:
            raise ValueError("Invalid role")
        return value
    
class RegisterResponse(BaseModel):
    id:int
    name:str
    email:EmailStr
    phone:str
    role : str

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    email : EmailStr
    password : str
    role : str = None
        
    
class RoleSchema(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    # class Config:
    #     from_attributes = True
        
class AuthMeResponse(BaseModel):
    id :int
    name : str
    email :EmailStr
    phone :Optional[str] = None
    roles : Optional[List[RoleSchema]] = []
    carts : Optional[list[None]] = []
    orders : Optional[list[None]] = []
    class Config:
        # populate_by_name = True
        from_attributes = True