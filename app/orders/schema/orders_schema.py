from pydantic import BaseModel
from typing import Optional, Any

class OrderBaseSchema(BaseModel):
    id : Optional[int] = None
    user_id : Optional[int] = None
    total_amount : Optional[int] = None
    status : Optional[str] = None

    
class OrderItemsBaseSchema(BaseModel):
    id : Optional[int] = None
    order_id : Optional[int] = None
    food_item_id : Optional[int] = None
    quantity : Optional[int] = None
    item_price : Optional[int] = None

    