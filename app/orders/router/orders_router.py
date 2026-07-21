from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.utility.auth_utility import require_customer
from app.orders.schema.orders_schema import GetOrderRequestSchema
from app.orders.service.orders_service import (
    post_order_service, get_id_order_service, get_orders_history_service
)

orders_router = APIRouter()


@orders_router.post('/post/order')
def post_order(db:Session = Depends(get_db),
               user = Depends(require_customer)
               ):
    response_data = post_order_service(db,user)
    return response_data

@orders_router.get('/get/order/{id:int}')
def get_id_order(id:int,
                 db:Session=Depends(get_db),
                 user=Depends(require_customer)
                 ):
    response_data = get_id_order_service(id,db,user)
    return response_data

@orders_router.post('/get/orders/history')
def get_orders_history(body:GetOrderRequestSchema,
                       db:Session=Depends(get_db),
                       user=Depends(require_customer)
                       ):
    response_data = get_orders_history_service(body,db,user)
    return response_data
