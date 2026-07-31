from datetime import datetime
import os 
import time
import json
import razorpay
from dotenv import load_dotenv
from fastapi import HTTPException, Request, status
from app.utility.enums import OrderStatusEnum, PaymentStatusEnum, RazorpayWebhookEvent
from app.models.common_models import Payment, PaymentEvent, IdempotencyKey
from app.utility.payment_utility import razorpay_client
from app.payments.schema.payments_schema import VerifyPaymentRequestSchema
from app.utility.enums import PaymentEventEnum, GatewayEnum
from fastapi.templating import Jinja2Templates
from app.utility.logger_utility import logger

load_dotenv()
template = Jinja2Templates(directory="app/payments/templates")

def create_payment_service(body, db, user):
    order_id = body.order_id
    orders = {order.id :order for order in user.orders}
    if order_id not in orders:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='ORDER NOT FOUND')
    order = orders[order_id]
    if order.status != OrderStatusEnum.PENDING:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='ORDER IS NOT PAYABLE')
    if order.total_amount <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='ORDER AMOUNT SHOULD BE GREATER THAN ZERO')  
    payments = (db.query(Payment)            # payment_method = 'ONLINE',
                .filter(Payment.order_id == order_id)
                .with_for_update()
                .first()
                )
    if payments is not None:
        if payments.status == PaymentStatusEnum.PENDING:
            return {
                "payment_id": payments.id,
                "id": payments.gateway_order_id,
                "amount": payments.amount * 100,
                "currency": payments.currency
            }
        if payments.status not in (PaymentStatusEnum.CANCELLED, PaymentStatusEnum.FAILED):
               raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                   detail='AN PAYMENT IS ALREADY PROCESSED')
    payment_details ={
        "amount" : order.total_amount * 100,
        "currency" : "INR",
        "receipt" : f"FF-{int(time.time())}-{order.id}",
        "partial_payment":False
    }
    data = razorpay_client.order.create(payment_details)
    try:
        payment = Payment(
            order_id = order_id,
            amount= order.total_amount,
            gateway = GatewayEnum.RAZORPAY,
            gateway_order_id = data.get("id"),
            currency = data.get("currency"),
            status = PaymentStatusEnum.PENDING
        )
        db.add(payment)
        db.flush()
        
        payment_event = PaymentEvent(payment_id = payment.id,
            event_type = PaymentEventEnum.GATEWAY_ORDER_CREATED,
            status = PaymentStatusEnum.PENDING,
            request_payload= payment_details,
            response_payload= json.dumps(data)
        )
        db.add(payment_event)
        db.commit()
        data['payment_id'] = payment.id
        return data
    except Exception as e:
        db.rollback()
        return f"{e}"
        
        
def verify_payment_service(body:VerifyPaymentRequestSchema, db):
    payment = db.query(Payment).filter(Payment.id == body.payment_id).first()
    if payment is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='not found')
    if payment.status in(PaymentStatusEnum.SUCCESS,):
        return True
    try:
        razorpay_client.utility.verify_payment_signature(
            body.model_dump(exclude='payment_id')
            )
        gateway_payment = razorpay_client.payment.fetch(body.razorpay_payment_id)
        if gateway_payment.get("order_id") != payment.gateway_order_id:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='INVALID ORDER ID')
        
        status = gateway_payment.get("status")
        if status == "captured":
            payment.status = PaymentStatusEnum.SUCCESS
            payment.order.status = OrderStatusEnum.PREPARING
        elif status == "failed":
            payment.status = PaymentStatusEnum.FAILED
        else:
            raise HTTPException(status_code=400,
                                detail=f"Payment is not complete. Current status: {status}")
                
        payment.gateway_payment_id = gateway_payment.get("id")
        payment.payment_method = gateway_payment.get("method")
        # payment.status = PaymentStatusEnum.SUCCESS
        
        payment_event = PaymentEvent(
            payment_id = payment.id,
            event_type = PaymentEventEnum.PAYMENT_SUCCESS,
            status = PaymentStatusEnum.SUCCESS,
            request_payload = body.model_dump(),
            response_payload = json.dumps(gateway_payment)
        )
        db.add(payment_event)
        db.commit()
        return True
    except razorpay.errors.SignatureVerificationError:
        db.rollback()
        return "Invalid payment signature"
    except Exception as e:
        db.rollback()
        return{"status":False,
               "message":f"{e}"}
        

async def payment_webhook_service(request:Request, x_razorpay_signature, x_razorpay_event_id, db):
    raw_body = await request.body()
    signature = x_razorpay_signature
    event_id = x_razorpay_event_id
    body = raw_body.decode("utf-8")
    payload =  json.loads(body)
    data = payload["payload"]["payment"]["entity"]
    
    try:
        razorpay_client.utility.verify_webhook_signature(body,signature,os.getenv('WEBHOOK_SECRET'))
        i_key = db.query(IdempotencyKey).filter(IdempotencyKey.key == event_id).first()
        if i_key:
            logger.info("Duplicate webhook ignored")
            return 
        payment = (db.query(Payment)
                   .filter(Payment.gateway_order_id == data.get("order_id"))
                   .with_for_update()
                   .first())
        if not payment:
            logger.error(
                        "Webhook received for unknown gateway order %s",
                        data.get("order_id"),
                    )
            return 
        pay_event = PaymentEvent(
            payment_id = payment.id,
            event_type = payload.get("event"),
            status = data.get("status"),
            request_payload = payload,
        )
        idemp_key = IdempotencyKey(
            key = event_id,
            payment_id = payment.id,
            endpoint = payload.get("event"),
        )  
        payment.payment_method = data.get("method")
        payment.gateway_payment_id = data.get("id")
        
        if payload["event"] == RazorpayWebhookEvent.PAYMENT_CAPTURED:
            timestamp = data.get("created_at")
            payment.status = PaymentStatusEnum.SUCCESS
            payment.paid_at = datetime.fromtimestamp(timestamp)
            payment.order.status = OrderStatusEnum.PREPARING
            
        elif payload["event"] == RazorpayWebhookEvent.PAYMENT_AUTHORIZED:
            payment.status = PaymentStatusEnum.PROCESSING
            
        elif payload["event"] == RazorpayWebhookEvent.PAYMENT_FAILED:
            payment.status = PaymentStatusEnum.FAILED
            payment.failure_reason = data.get("error_reason")
            
        db.add_all([pay_event, idemp_key])
        db.commit()
        return True
    except razorpay.errors.SignatureVerificationError:
        db.rollback()
        raise HTTPException(status_code=401, detail="Invalid webhook signature")
    except Exception as e:
        logger.exception(f"{e}")
        db.rollback()
        return {e}