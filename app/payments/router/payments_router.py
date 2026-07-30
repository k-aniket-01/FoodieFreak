from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.payments.schema.payments_schema import CreatePaymentRequestSchema, VerifyPaymentRequestSchema
from app.utility.auth_utility import require_customer
from app.database import get_db
from app.payments.service.payments_service import create_payment_service, verify_payment_service
import os 
from dotenv import load_dotenv

load_dotenv()

payment_router = APIRouter()

template = Jinja2Templates(directory="app/payments/templates")

@payment_router.post('/payment/create')
def create_payment(body:CreatePaymentRequestSchema,
                   db:Session = Depends(get_db),
                   user=Depends(require_customer)
                   ):
    response_data = create_payment_service(body,db,user)
    return response_data

@payment_router.post('/payment/verify')
def verify_payment(body:VerifyPaymentRequestSchema,
                   db:Session=Depends(get_db),
                   ):
    response_data = verify_payment_service(body, db)
    return response_data


#temp outers below don not commit/ or reomve after this module finsinshed
@payment_router.get('/temp/login')
def temp_login(request:Request):
    return template.TemplateResponse(request=request,
                                     name='login.html',
                                     )
    
    
@payment_router.get('/payment/checkout')
def checkout_payment(reqeust:Request):
    return template.TemplateResponse(request=reqeust,
                                     name='index.html',
                                     context={"key_id":os.getenv("RAZORPAY_KEY_ID")})
    
@payment_router.get('/payment/success')
def successful_payment(request:Request):
    return template.TemplateResponse(request=request,
                                     name='success.html')