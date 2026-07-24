from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.utility.auth_utility import require_customer, require_owner
from app.utility.enums import OrderStatusEnum
from app.orders.schema.orders_schema import GetOrderRequestSchema, GetCanteenOrdersRequestSchema
from app.orders.service.orders_service import (
    post_order_service, get_id_order_service, get_orders_history_service, cancel_order_service,
    get_order_status_service, get_active_orders_service, get_canteen_orders_service,
    get_canteen_orders_details_service, patch_canteen_order_status_service
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

@orders_router.patch('/order/{id:int}/cancel')
def cancel_order(id:int,
                 db:Session=Depends(get_db),
                 user=Depends(require_customer)
                 ):
    response_data = cancel_order_service(id,db,user)
    return response_data

@orders_router.get('/order/{id:int}/status')
def get_order_status(id:int,
                     db:Session=Depends(get_db),
                     user=Depends(require_customer)
                     ):
    response_data = get_order_status_service(id,db,user)
    return response_data

@orders_router.get('/get/orders/active')
def get_active_orders(db:Session=Depends(get_db),
                      user=Depends(require_customer)
                      ):
    response_data = get_active_orders_service(db,user)
    return response_data

@orders_router.get('/get/canteen/orders')
def get_canteen_orders(db : Session = Depends(get_db),
                       user = Depends(require_owner),
                       filters: GetCanteenOrdersRequestSchema = Depends()
                       ):
    response_data = get_canteen_orders_service(db, user, filters)
    return response_data

@orders_router.get('/canteen/order{id:int}')
def get_canteen_order_details(id:int,
                              db:Session=Depends(get_db),
                              user=Depends(require_owner)
                              ):
    response_data = get_canteen_orders_details_service(id, db, user)
    return response_data

@orders_router.patch('/patch/canteen/order/{id:int}/prepare')
def patch_canteen_order_prepare(id:int,
                                db:Session=Depends(get_db),
                                user=Depends(require_owner)
                                ):
    transition = OrderStatusEnum.PREPARING
    response_data = patch_canteen_order_status_service(id,db,transition)
    return response_data

@orders_router.patch('/patch/canteen/order/{id:int}/ready')
def patch_canteen_order_ready(id:int,
                              db:Session=Depends(get_db),
                              user=Depends(require_owner)
                              ):
    transition = OrderStatusEnum.READY
    response_data = patch_canteen_order_status_service(id,db,transition)
    return response_data

@orders_router.patch("/patch/canteen/order/{id:int}/complete")
def patch_canteen_order_complete(id:int,
                                 db:Session=Depends(get_db),
                                 user=Depends(require_owner)
                                 ):
    transition = OrderStatusEnum.COMPLETED
    response_data = patch_canteen_order_status_service(id,db,transition)
    return response_data

@orders_router.patch('/patch/canteen/order/{id:int}/cancel')
def patch_canteen_order_cancel(id:int,
                               db:Session=Depends(get_db),
                               user=Depends(require_owner)
                               ):
    transition = OrderStatusEnum.CANCELLED
    response_data = patch_canteen_order_status_service(id,db,transition)
    return response_data