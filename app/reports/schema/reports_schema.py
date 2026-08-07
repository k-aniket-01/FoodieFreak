from pydantic import BaseModel
from typing import Optional

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
    