import time
import json
from fastapi import HTTPException,status
from app.utility.enums import OrderStatusEnum, PaymentStatusEnum
from app.models.common_models import Payment, PaymentEvent
from app.utility.payment_utility import razorpay_client
from app.utility.enums import PaymentEventEnum, GatewayEnum


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
                     .first()
                     )
    if payments is not None:
        if payments.status not in (PaymentStatusEnum.CANCELLED, PaymentStatusEnum.FAILED):
               raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                   detail='AN PAYMENT IS ALREADY PROCESSED')
    payment_details ={
        "amount" : order.total_amount,
        "currency" : "INR",
        "receipt" : f"FF-{int(time.time())}-{order.id}",
        "partial_payment":False
    }
    data = razorpay_client.order.create(payment_details)
    print(data)
    try:
        payment = Payment(
            order_id = order_id,
            amount= order.total_amount,
            payment_method = 'ONLINE',
            gateway = GatewayEnum.RAZORPAY,
            gateway_order_id = data.get("id"),
            # gateway_payment_id = 
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
        return data
    except Exception as e:
        db.rollback()
        return f"{e}"
        
        