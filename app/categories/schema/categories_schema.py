from pydantic import BaseModel
from typing import Optional, Any

class CategoriesBaseSchema(BaseModel):
    id : Optional[Any] = None
    name : Optional[Any] = None
    description : Optional[Any] = None
    is_active : Optional[Any] = None
    food_items : Optional[Any] = None

class PostCategoriesRequestSchema(BaseModel):
    name : str
    description : Optional[Any] = None 
    
class GetCategoriesResponseSchema(CategoriesBaseSchema):
    pass
class PutCategoryIdSchema(PostCategoriesRequestSchema):
    pass