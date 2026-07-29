from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.payments.schema.payments_schema import CreatePaymentRequestSchema
from app.utility.auth_utility import require_customer
from app.database import get_db
from app.payments.service.payments_service import create_payment_service

payment_router = APIRouter()

@payment_router.post('/payment/create')
def create_payment(body:CreatePaymentRequestSchema,
                   db:Session = Depends(get_db),
                   user=Depends(require_customer)
                   ):
    response_data = create_payment_service(body,db,user)
    return response_data
