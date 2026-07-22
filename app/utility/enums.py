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