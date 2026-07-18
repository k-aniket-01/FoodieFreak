from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.utility.auth_utility import require_customer
from app.carts.service.carts_service import (
    post_cart_item_service, get_cart_items_service,put_cart_item_service,
    delete_cart_item_service, clear_cart_items_service
)
from app.carts.schema.carts_schema import PostCartItemRequestSchema, PutCartItemRequestBody

carts_router = APIRouter()

@carts_router.post('/post/cart/item')
def post_cart_item(body:PostCartItemRequestSchema,
                   db:Session=Depends(get_db),
                   user=Depends(require_customer)
                   ):
    response_data = post_cart_item_service(body,db,user)
    return response_data

@carts_router.get('/get/cart/items')
def get_cart_items(db:Session = Depends(get_db),
                   user=Depends(require_customer)
                   ):
    response_data = get_cart_items_service(db, user)
    return response_data

@carts_router.put('/put/cart/item/{id:int}')
def put_cart_item(id:int,
                  body:PutCartItemRequestBody,
                  db:Session=Depends(get_db),
                  user=Depends(require_customer)
                  ):
    response_data = put_cart_item_service(id,body,db,user)
    return response_data

@carts_router.delete('/delete/cart/item/{id:int}')
def delete_cart_item(id:int,
                     db:Session=Depends(get_db),
                     user=Depends(require_customer)
                     ):
    response_data = delete_cart_item_service(id,db,user)
    return response_data

@carts_router.delete('/clear/cart/items')
def clear_cart_itmes(db:Session=Depends(get_db),
                     user = Depends(require_customer)
                     ):
    response_data = clear_cart_items_service(db,user)
    return response_data