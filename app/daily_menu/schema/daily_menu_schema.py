from pydantic import BaseModel
from typing import Optional,Any
from datetime import date

class DailyMenuBaseSchema(BaseModel):
    id : Optional[int] = None
    food_item_id : Optional[int] = None
    menu_date : Optional[str] = None
    available_qty : Optional[int] = None
    is_available : Optional[bool] = None
    food_item : Optional[Any] = None
    
class FoodItemSchema(BaseModel):
    food_item_id : Optional[int] = None
    available_qty : Optional[int] = None
    
class DailyMenuRequestSchema(BaseModel):
    menu_date : Optional[str] = date.today()
    food_items : Optional[list[FoodItemSchema]] = None
    
    