from pydantic import BaseModel, ConfigDict
from typing import Optional,Any
from app.categories.schema.categories_schema import CategoriesBaseSchema

class FoodItemsBaseSchema(BaseModel):
    id : Optional[int] = None
    name : Optional[str] = None
    description : Optional[str] = None
    price : Optional[int] = None
    is_active : Optional[Any] = None
    category_id : Optional[int] = None
    category : Optional[Any] = None
    
class FoodItemRequestSchema(BaseModel):
    name : str
    description : Optional[str] = None
    price : Optional[int] = None
    category_id : int
    
class CategorySubSchema(BaseModel):
    id : Optional[Any] = None
    name : Optional[Any] = None
    description : Optional[Any] = None
    is_active : Optional[Any] = None

    
class GetFoodItemsResponseSchema( FoodItemsBaseSchema):
    category : CategorySubSchema | None = None

class PatchFoodAvailabilityRequestSchema(BaseModel):
    is_available : bool