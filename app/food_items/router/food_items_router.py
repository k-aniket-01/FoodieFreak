from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.utility.auth_utility import require_owner
from app.food_items.schema.food_items_schema import FoodItemRequestSchema, PatchFoodAvailabilityRequestSchema
from app.food_items.service.food_items_service import (
    post_food_items_service, get_food_items_service, get_food_item_id_service, 
    put_food_item_id_service, delete_food_item_service, patch_food_availability_service
)
food_items_router = APIRouter()

@food_items_router.post('/post/food/items')
def post_food_items(body:FoodItemRequestSchema,
                    user=Depends(require_owner),
                    db:Session=Depends(get_db),
                    ):
    response = post_food_items_service(body, db)
    return response

@food_items_router.get('/get/food/items')
def get_food_items(db:Session=Depends(get_db)
                   ):
    response = get_food_items_service(db)
    return response

@food_items_router.get('/get/food/item/{id:int}')
def get_food_item_id(id:int,
                     db:Session=Depends(get_db)
                     ) -> bool:
    response = get_food_item_id_service(id, db)
    return response

@food_items_router.put('/put/food/item/{id:int}')
def put_food_item_id(id:int,
                     body:FoodItemRequestSchema,
                     user = Depends(require_owner),
                     db:Session=Depends(get_db)
                     ):
    response = put_food_item_id_service(id,body,db)
    return response

@food_items_router.delete('/delete/food/item/{id:int}')
def delete_food_item(id:int,
                     user=Depends(require_owner),
                     db:Session=Depends(get_db)
                     ):
    response = delete_food_item_service(id,db)
    return response

@food_items_router.patch('/patch/foods/{id:int}/availability')
def patch_food_availability(id:int,
                            body:PatchFoodAvailabilityRequestSchema,
                            user=Depends(require_owner),
                            db:Session = Depends(get_db)
                            ):
    response = patch_food_availability_service(id,body,db)
    return response
