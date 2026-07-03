from pydantic import BaseModel
from typing import Optional, Any


class UserProfileResponseSchema(BaseModel):
    id : Optional[int] = None 
    name : Optional[str] = None 
    email : Optional[str] = None 
    phone : Optional[str] = None 
    created_at : Optional[Any] = None 