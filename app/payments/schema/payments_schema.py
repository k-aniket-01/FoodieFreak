from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from app.utility.enums import PaymentStatusEnum, PaymentSortByEnum, SortEnum
from app.utility.response_utility import PaginationResponseSchema

class PaymentBaseSchema(BaseModel):
    id : Optional[int] = None
    order_id : Optional[int] = None
    gateway : Optional[str] = None
    gateway_order_id : Optional[str] = None
    gateway_payment_id : Optional[str] = None
    amount : Optional[int] = None
    currency : Optional[str] = None
    payment_method : Optional[str] = None
    status : Optional[str] = None
    failure_reason : Optional[str] = None
    paid_at : Optional[datetime] = None
    created_at : Optional[datetime] = None
    updated_at : Optional[datetime] = None
    
class CreatePaymentRequestSchema(BaseModel):
    order_id : int
    
class VerifyPaymentRequestSchema(BaseModel):
    payment_id: int
    razorpay_order_id : str
    razorpay_payment_id : str
    razorpay_signature : str
    
class GetPaymentHistoryFiltersSchema(BaseModel):
    page: int = 1
    per_page: int = 10
    id : int | None = None
    gateway_order_id : str | None = None
    gateway_payment_id : str | None = None
    amount : int | None = None
    status: PaymentStatusEnum | None = None
    order_id: int | None = None
    start_date: date | None = None
    end_date: date | None = None
    sort_by: PaymentSortByEnum = PaymentSortByEnum.paid_at
    sort_order: SortEnum = SortEnum.DESC
    
class GetPaymentHistoryResponseSchema(BaseModel):
    data : list[PaymentBaseSchema] = None
    pagination : PaginationResponseSchema = None
    
class RefundRequestSchema(BaseModel):
    payment_id : int
    reason : Optional[str] = None
    