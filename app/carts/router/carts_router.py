from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.utility.auth_utility import require_customer
from app.carts.service.carts_service import post_cart_item_service
from app.carts.schema.carts_schema import PostCartItemRequestSchema

carts_router = APIRouter()

@carts_router.post('/post/cart/item')
def post_cart_item(body:PostCartItemRequestSchema,
                   db:Session=Depends(get_db),
                   user=Depends(require_customer)
                   ):
    response_data = post_cart_item_service(body,db,user)
    return response_data
