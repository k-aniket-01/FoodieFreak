from app.reports.schema.reports_schema import (
    DashboardStatsResponseSchema, DashbardRevenueResponseSchema, RevenueByDateSchema, 
    DashboardRevenueParamSchema
)

def get_dashboard_stats_transformer(
    orders, revenue, total_customers, todays_menu_items
):
    
    data_dict = {
        "total_orders" : orders[0],
        "todays_orders" : orders[1],
        "active_orders" : orders[2],
        "completed_orders" : orders[3],
        "cancelled_orders" : orders[4],
        "todays_revenue" : revenue[0],
        "total_revenue" : revenue[1],
        "total_customers": total_customers,
        "todays_menu_items": todays_menu_items
    }
    response_data = (
        DashboardStatsResponseSchema
        .model_validate(data_dict, from_attributes=True)
        .model_dump()
    )
    return response_data


def dashboard_revenue_transformer(params:DashboardRevenueParamSchema, revenue, revenue_by_date):
    params = params.model_dump()
    revenue = dict(revenue._mapping)
    revenue_by_date = [
        RevenueByDateSchema
        .model_validate(item, from_attributes=True)
        .model_dump()
        for item in revenue_by_date
    ]
    data = {**params, **revenue, "revenue_by_date":revenue_by_date}
    response_date = (
        DashbardRevenueResponseSchema
        .model_validate(data)
        .model_dump()
    )
    return response_date
