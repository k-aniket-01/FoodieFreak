from enum import Enum

class OrderStatusEnum(str, Enum):
    PENDING = "PENDING"
    PREPARING = "PREPARING"
    READY = "READY"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    
class FilterOrderStatusEnum(str, Enum):
    ALL = "ALL"
    PENDING = "PENDING"
    PREPARING = "PREPARING"
    READY = "READY"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    
class SortEnum(str, Enum):
    ASC = "asc" 
    DESC = "desc"
    
class CanteenOrderSortByEnum(str, Enum):
    ID = "id"
    USER_ID = "user_id"
    TOTAL_ITEMS = "total_items"
    CREATED_AT = "created_at"
    STATUS = "status"
    TOTAL_AMOUNT = "total_amount"
    
class PaymentStatusEnum(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    REFUNDED = "REFUNDED"
    
class PaymentEventEnum(str, Enum):
    PAYMENT_CREATED = "PAYMENT_CREATED"
    GATEWAY_ORDER_CREATED = "GATEWAY_ORDER_CREATED"
    PAYMENT_SUCCESS = "PAYMENT_SUCCESS"
    PAYMENT_FAILED = "PAYMENT_FAILED"
    WEBHOOK_RECEIVED = "WEBHOOK_RECEIVED"
    WEBHOOK_VERIFIED = "WEBHOOK_VERIFIED"
    REFUND_CREATED = "REFUND_CREATED"