from app.reports.schema.reports_schema import DashboardStatsResponseSchema

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
