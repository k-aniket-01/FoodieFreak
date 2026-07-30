from pydantic import BaseModel
from typing import Optional
class CreatePaymentRequestSchema(BaseModel):
    order_id : int
    
class VerifyPaymentRequestSchema(BaseModel):
    payment_id: int
    razorpay_order_id : str
    razorpay_payment_id : str
    razorpay_signature : str
    