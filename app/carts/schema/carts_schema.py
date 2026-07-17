from pydantic import BaseModel
from typing import Optional,Any

class CartItemBaseSchema(BaseModel):
    id : Optional [int] = None
    cart_id : Optional [int] = None
    food_item_id : Optional [int] = None
    quantity : Optional [int] = None
    cart : Optional [Any] = None
    food_item : Optional [Any] = None
    
class PostCartItemRequestSchema(BaseModel):
    food_item_id : int
    quantity : int
    