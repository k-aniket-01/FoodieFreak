from pydantic import BaseModel
from typing import Optional


class NotificationBaseSchema(BaseModel):
    id : Optional[int] = None
    user_id : Optional[int] = None
    title : Optional[str] = None
    message : Optional[str] = None
    is_read : Optional[bool] = None
    
    
class GetNotificationResponseSchema(NotificationBaseSchema):
    class Config:
        from_attributes = True