from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from app.utility.enums import OrderStatusEnum, FilterOrderStatusEnum, SortEnum, CanteenOrderSortByEnum
from app.utility.response_utility import PaginationRequestSchema, PaginationResponseSchema

class OrderBaseSchema(BaseModel):
    id : Optional[int] = None
    user_id : Optional[int] = None
    total_items : Optional[int] = None
    total_amount : Optional[int] = None
    status : Optional[OrderStatusEnum] = None
    created_at : Optional[datetime] = None

    
class OrderItemsBaseSchema(BaseModel):
    id : Optional[int] = None
    order_id : Optional[int] = None
    food_item_id : Optional[int] = None
    quantity : Optional[int] = None
    item_price : Optional[int] = None

class OrderSummerySchema(BaseModel):
    order_id : Optional[int] = None
    user_id : Optional[int] = None
    status : Optional[OrderStatusEnum] = None 
    total_items : Optional[int] = None
    total_amount : Optional[int] = None
    
class GetOrderItemsSchema(BaseModel):
    # order_id : Optional [int] = None 
    food_item_id : Optional [int] = None 
    food_name : Optional [str] = None 
    quantity : Optional [int] = None 
    item_price : Optional [int] = None 
    sub_total : Optional [int] = None     
    
class GetOrderIdResponseSchema(OrderSummerySchema):
    items : list[GetOrderItemsSchema] = []
    
class GetOrderRequestSchema(BaseModel):
    id : Optional[int] = None
    status : Optional[OrderStatusEnum] = None
    pagination: Optional[PaginationRequestSchema] = None
    
class GetOrderHistoryResponseSchema(PaginationResponseSchema):
    orders : list[OrderBaseSchema] = None
    
class GetOrderStatusResponseSchema(BaseModel):
    id : Optional[int] = None
    status : Optional[OrderStatusEnum] = None
    created_at : Optional[datetime] = None
    
    
class GetCanteenOrdersRequestSchema(BaseModel):
    page: int = 1
    per_page: int = 10
    status: FilterOrderStatusEnum = FilterOrderStatusEnum.ALL
    customer_id: int | None = None
    order_id: int | None = None
    start_date: date | None = None
    end_date: date | None = None
    sort_by: CanteenOrderSortByEnum = CanteenOrderSortByEnum.CREATED_AT
    sort_order: SortEnum = SortEnum.DESC
    
class ItemsSchema(BaseModel):
    food_item_id : Optional[int] = None
    food_name : Optional[str] = None
    quantity : Optional[int] = None
    price : Optional[int] = None
    sub_total : Optional[int] = None    
    
class CustomerSchema(BaseModel):
    customer_id : Optional[int] = None
    customer_name : Optional[str] = None
    customer_email : Optional[str] = None
    
class GetCanteenSummerySchema(BaseModel):
    id : Optional[int] = None
    status : Optional[str] = None
    total_items : Optional[int] = None
    total_amount : Optional[int] = None
    created_at : Optional[datetime] = None

class GetCanteenOrderDetailResponseSchema(GetCanteenSummerySchema):
    customer : Optional[CustomerSchema] = None
    items : Optional[list[ItemsSchema]] = None