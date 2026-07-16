from pydantic import BaseModel
from typing import Optional,Any
from datetime import date
from app.utility.response_utility import PaginationRequestSchema

class DailyMenuBaseSchema(BaseModel):
    menu_date : Optional[date] = None
    id : Optional[int] = None
    food_item_id : Optional[int] = None
    available_qty : Optional[int] = None
    is_available : Optional[bool] = None
    food_item : Optional[Any] = None
    
class FoodItemSchema(BaseModel):
    food_item_id : Optional[int] = None
    available_qty : Optional[int] = None
    
class DailyMenuRequestSchema(BaseModel):
    menu_date : Optional[date] = date.today()
    food_items : Optional[list[FoodItemSchema]] = None
    
class DailyMenuResponseSchema(DailyMenuBaseSchema):
    class Config:
        from_attributes = True    
        
class PutDailyMenuRequestSchema(BaseModel):
    menu_date : Optional[date] = date.today()
    available_qty : Optional[int] = None
    is_available : Optional[bool] = None

    
class DailyMenuHistoryRequestSchema(BaseModel):
    menu_date : Optional[date] = None
    id : Optional[int] = None
    food_item_id : Optional[int] = None
    is_available : Optional[bool] = None
    pagination : Optional[PaginationRequestSchema] = None