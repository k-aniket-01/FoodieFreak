from pydantic import BaseModel
from typing import Optional, Any

class UserBaseSchema(BaseModel):
    id : Optional[int] = None 
    name : Optional[str] = None 
    email : Optional[str] = None 
    phone : Optional[str] = None 
class UserProfileResponseSchema(UserBaseSchema):
    is_active : Optional[Any] = None
    created_at : Optional[Any] = None 
    
class UserProfileUpdateRequestSchema(BaseModel):
    name : Optional[str] = None 
    email : Optional[str] = None 
    phone : Optional[str] = None 

class UserProfileUpdateResponseSchema(UserProfileResponseSchema):
    pass