from app.reports.schema.reports_schema import (
    DashboardStatsResponseSchema, DashboardRevenueResponseSchema, RevenueByDateSchema, 
    ReportParamSchema, OrderTrend, DashBoardOrdersResponseSchema, StatusSummary, CustomerStatsSummery,
    CustomerStatTopCustomers, CustomerStatsResponseSchema, CustomerStatCustomerGrowth
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


def dashboard_revenue_transformer(
    params: ReportParamSchema, revenue, revenue_by_date
):
    params = params.model_dump(exclude=["pdf"])
    revenue = dict(revenue._mapping)
    revenue_by_date = [
        RevenueByDateSchema.model_validate(item, from_attributes=True).model_dump()
        for item in revenue_by_date
    ]
    data = {**params, **revenue, "revenue_by_date": revenue_by_date}
    response_date = DashboardRevenueResponseSchema.model_validate(data).model_dump()
    return response_date


def dashboard_orders_transformer(params: ReportParamSchema, summery, order_trend):
    params = params.model_dump(exclude=["pdf"])
    total_order = dict(summery._mapping)
    status_summary = StatusSummary.model_validate(summery, from_attributes=True).model_dump()
    order_trend = [
        OrderTrend.model_validate(item, from_attributes=True).model_dump()
        for item in order_trend
    ]
    data = {
        **params,
        **total_order,
        "status_summary": status_summary,
        "order_trend": order_trend,
    }
    response_data = DashBoardOrdersResponseSchema.model_validate(data).model_dump()
    return response_data


def customer_stats_transformer(params:ReportParamSchema, summary, top_customers, customer_growth):
    params = params.model_dump(exclude={"pdf"})
    summary = CustomerStatsSummery.model_validate(
        summary, from_attributes=True
    ).model_dump()
    
    top_customers = [
        CustomerStatTopCustomers.model_validate(data, from_attributes=True).model_dump()
        for data in top_customers
    ]
    
    customer_growth = [
        CustomerStatCustomerGrowth.model_validate(data, from_attributes=True).model_dump()
        for data in customer_growth
    ]

    data = {
        **params, 
        "summery":summary, 
        "top_customers":top_customers, 
        "customer_growth":customer_growth
        }
    
    response_data = CustomerStatsResponseSchema.model_validate(
        data, from_attributes=True
    ).model_dump()
    
    return response_data
