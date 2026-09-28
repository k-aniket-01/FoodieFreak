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
    
class ReportParamSchema(BaseModel):
    start_date : Optional[date | None] = None
    end_date : Optional[date | None] = None  
    pdf: Optional[bool] = False
    
class DateParamResSchema(BaseModel):
    start_date : Optional[date | None] = None
    end_date : Optional[date | None] = None  

class RevenueByDateSchema(BaseModel):
    r_date : Optional[date | None] = None 
    revenue : Optional[int | None] = 0
    transactions : Optional[int | None] = 0
    
class DashboardRevenueResponseSchema(DateParamResSchema):
    total_revenue : Optional[int | None] = 0
    total_transactions : Optional[int | None] = 0
    average_order_value : Optional[int | None] = 0
    revenue_by_date : list[RevenueByDateSchema] | None = []
    
class StatusSummary(BaseModel):
    pending : Optional[int] = None
    preparing : Optional[int] = None
    ready : Optional[int] = None
    completed : Optional[int] = None
    cancelled : Optional[int] = None    

class OrderTrend(BaseModel):
    t_date : Optional[date] = None
    orders : Optional[int] = None

class DashBoardOrdersResponseSchema(DateParamResSchema):
    total_orders : Optional[int] = None
    status_summary : StatusSummary
    order_trend : list[OrderTrend] = []
    
class CustomerStatsSummery(BaseModel):
    total_customers : Optional[int] = None
    active_customers : Optional[int] = None
    customer_with_orders : Optional[int] = None
    customer_wout_orders : Optional[int] = None
    total_orders : Optional[int] = None
    avg_orders : Optional[int] = None
    total_spendings : Optional[int] = None    
    
class CustomerStatTopCustomers(BaseModel):
    id : Optional[int] = None
    name : Optional[str] = None
    total_orders : Optional[int] = 0
    total_spent : Optional[int] = 0
    
class CustomerStatCustomerGrowth(BaseModel):
    period : Optional[str] = None
    new_customers : Optional[int] = 0
    
class CustomerStatsResponseSchema(DateParamResSchema):
    summery : CustomerStatsSummery = {}
    top_customers : list[CustomerStatTopCustomers] = []
    customer_growth : list[CustomerStatCustomerGrowth] = []
    