from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.utility.auth_utility import require_customer
from app.orders.service.orders_service import post_order_service, get_id_order_service


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