import os 
import json
import time
import razorpay
from datetime import datetime
from dotenv import load_dotenv
from app.utility.logger_utility import logger
from fastapi.templating import Jinja2Templates
from fastapi import HTTPException, Request, status
from app.utility.payment_utility import razorpay_client
from app.utility.enums import PaymentEventEnum, GatewayEnum
from app.utility.enums import OrderStatusEnum, PaymentStatusEnum, RazorpayWebhookEvent
from app.utility.response_utility import apply_filters, apply_pagination, apply_sorting
from app.models.common_models import Payment, PaymentEvent, IdempotencyKey,Order, User, Refund
from app.payments.schema.payments_schema import VerifyPaymentRequestSchema, RefundRequestSchema
from app.payments.transformer.payments_transformer import get_payment_history_transformer, get_payment_transformer

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
    payments = (db.query(Payment)
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
        
        payment_event = PaymentEvent(
            payment_id = payment.id,
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
        

async def payment_webhook_service(request: Request, x_razorpay_signature, x_razorpay_event_id, db):
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
            logger.info("Duplicate webhook ignored %s", i_key)
            return 
        payment = (db.query(Payment)
                   .filter(Payment.gateway_order_id == data.get("order_id"))
                   .with_for_update()
                   .first())
        if not payment:
            logger.error("Webhook received for unknown gateway order %s", data.get("order_id"))
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
    

def get_payment_history_service(db, user, params):
    query = (db.query(Payment.id,
                      Payment.order_id,
                      Payment.gateway,
                      Payment.gateway_order_id,
                      Payment.gateway_payment_id,
                      Payment.amount,
                      Payment.currency,
                      Payment.payment_method,
                      Payment.status,
                      Payment.failure_reason,
                      Payment.paid_at,
                      Payment.created_at,
                      Payment.updated_at)
             .join(Order, Payment.order_id == Order.id)
             .join(User, Order.user_id == User.id)
            ) #below used the function to reduce repetative logic to check query without this
    query = query.filter(User.id == user.id) #check app/orders/service get_canteen_orders_service
    query = apply_sorting(body=params, model=Payment, query=query)
    query = apply_filters(body=params, model=Payment, query=query)
    query, pagination = apply_pagination(body=params, query=query)
    query = query.all()
    response_data = get_payment_history_transformer(query, pagination)
    return response_data


def get_payment_service(id, db, user):
    payment = (db.query(Payment.id,
                        Payment.order_id,
                        Payment.gateway,
                        Payment.gateway_order_id,
                        Payment.gateway_payment_id,
                        Payment.amount,
                        Payment.currency,
                        Payment.payment_method,
                        Payment.status,
                        Payment.failure_reason,
                        Payment.paid_at,
                        Payment.created_at,
                        Payment.updated_at)
                .join(Order, Payment.order_id == Order.id)
                .join(User, Order.user_id == User.id)
                .filter(User.id == user.id, Payment.id == id)
                .first()
                )
    if not payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='ORDER NOT FOUND')
    response_data = get_payment_transformer(payment)
    return response_data


def create_refund_service(body:RefundRequestSchema, db, user):
    payment = (
        db.query(Payment)
        .join(Order, Payment.order_id == Order.id)
        .join(User, Order.user_id == User.id)
        .filter(User.id == user.id, Payment.id == body.payment_id)
        .first()
        )
    print(payment)
    if not payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='PAYMENT DETAILS NOT FOUND')
    if payment.status != PaymentStatusEnum.SUCCESS:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='PAYMENT CANNOT BE REFUNDED')
    if payment.order.status not in (OrderStatusEnum.PENDING, OrderStatusEnum.PREPARING):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='PAYMENT CANNNOT BE REUNDED')
    refunds = db.query(Refund).filter(Refund.payment_id == body.payment_id).first()
    if refunds:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='AN REFUND ALREADY PROCESSED')
    try:
        refund_amount = int(payment.amount * 100)
        print(payment.gateway_payment_id)
        print(refund_amount)
        data = razorpay_client.payment.refund(
            payment.gateway_payment_id,
            {"amount":refund_amount, "speed":"normal"}
            )
        rec_refund = Refund(
            payment_id = payment.id,
            gateway_refund_id = data.get("id"),
            amount = data.get("amount") // 100,
            status = data.get("status"),
            speed_requested = data.get("speed_requested"),
            speed_processed = data.get("speed_processed")
            )
        pay_event = PaymentEvent(
            payment_id = payment.id,
            event_type = data.get("entity"),
            status = data.get("status"),
            request_payload = body.model_dump(),
            response_payload = json.dumps(data)
            )
        payment.status = PaymentStatusEnum.REFUND_CREATED
        payment.order.status = OrderStatusEnum.CANCELLED
        
        db.add_all([rec_refund, pay_event])
        db.commit()
        return True
    except razorpay.errors.BadRequestError  as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'{e}')
    except Exception as e:
        db.rollback()
        logger.error(f"{e}")
        raise e
    
    
async def refund_webhook_service(request:Request, x_razorpay_signature, x_razorpay_event_id, db):
        raw_body = await request.body()
        signature = x_razorpay_signature
        event_id = x_razorpay_event_id
        body = raw_body.decode("utf-8")
        payload =  json.loads(body)
        data = payload["payload"]["refund"]["entity"]
        logger.info('refund webhook received')
        
        try:
            razorpay_client.utility.verify_webhook_signature(body, signature, os.getenv('WEBHOOK_SECRET'))
            i_key = db.query(IdempotencyKey).filter(IdempotencyKey.key == event_id).first()
            if i_key:
                logger.info("Duplicate webhook ignored %s", i_key)
                return False
            refund = (db.query(Refund)
                      .filter(Refund.gateway_refund_id == data.get("id"))
                      .with_for_update()
                      .first()
                      )
            if not refund:
                logger.error("Webhook received for unknown gateway refund %s", data.get("id"))
                return False
            
            refund.status = data.get("status")
            refund.speed_requested = data.get("speed_requested")
            refund.speed_processed = data.get("speed_processed")
            
            pay_event = PaymentEvent(
                payment_id = refund.payment_id,
                event_type = payload.get("event"),
                status = data.get("status"),
                request_payload = payload
            )
            idem_key = IdempotencyKey(
                key = event_id,
                payment_id = refund.payment_id,
                endpoint = payload.get('event')
            )
            db.add_all([pay_event, idem_key])
            db.commit()
            return True
            
        except Exception as e:
            db.rollback()
            logger.error(e)
            raise e
        