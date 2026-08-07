from pydantic import BaseModel
from typing import Optional
from datetime import date

class DashboardStatsResponseSchema(BaseModel):
    total_orders : Optional[int] = None
    todays_orders : Optional[int] = None
    active_orders : Optional[int] = None
    completed_orders : Optional[int] = None
    cancelled_orders : Optional[int] = None
    todays_revenue : Optional[int] = None
    total_revenue : Optional[int] = None
    total_customers : Optional[int] = None
    todays_menu_items : Optional[int] = None
    
class DashboardRevenueParamSchema(BaseModel):
    start_date : Optional[date | None] = None
    end_date : Optional[date | None] = None  
    pdf: Optional[bool] = False
    
class RevenueByDateSchema(BaseModel):
    r_date : Optional[date | None] = None 
    revenue : Optional[int | None] = 0
    transactions : Optional[int | None] = 0
    
class DashbardRevenueResponseSchema(DashboardRevenueParamSchema):
    total_revenue : Optional[int | None] = 0
    total_transactions : Optional[int | None] = 0
    average_order_value : Optional[int | None] = 0
    revenue_by_date : list[RevenueByDateSchema] | None = []