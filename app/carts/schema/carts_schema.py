from pydantic import BaseModel
from typing import Optional,Any

class CartItemBaseSchema(BaseModel):
    cart : Optional [Any] = None
    id : Optional [int] = None
    cart_id : Optional [int] = None
    food_item_id : Optional [int] = None
    quantity : Optional [int] = None
    food_item : Optional [Any] = None
    
class PostCartItemRequestSchema(BaseModel):
    food_item_id : int
    quantity : int
    
class CartItemsSchema(BaseModel):
    id : Optional [int] = None
    food_item_id : Optional [int] = None
    name : Optional [str] = None
    price : Optional [int] = None
    quantity : Optional [int] = None
    sub_total : Optional [int] = None

class SummerySchema(BaseModel):
    cart_id : Optional[int] = None
    total_items : Optional[int] = None
    total_amount : Optional[int] = None
    
class GetCartResponseSchema(SummerySchema):
    items : list[CartItemsSchema] = []
    
class PutCartItemRequestBody(BaseModel):
    quantity : Optional[int] = None