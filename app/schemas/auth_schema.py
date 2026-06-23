from pydantic import BaseModel, EmailStr, Field, field_validator

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
        