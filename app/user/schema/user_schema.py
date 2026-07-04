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

class GetUserOrdersSchema(UserProfileResponseSchema):
    orders : Optional[Any] = None
    
class GetUserPaymentsSchema(BaseModel):
    id : Optional[Any] = None
    name : Optional[Any] = None
    email : Optional[Any] = None
    phone : Optional[Any] = None
    is_active : Optional[Any] = None
    order_id : Optional[Any] = None
    transaction_id : Optional[Any] = None
    payment_method : Optional[Any] = None
    status : Optional[Any] = None