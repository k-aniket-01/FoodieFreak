from datetime import date, datetime, time, timedelta
from app.models.common_models import DailyMenu, Order, Payment, User, UserRole
from app.utility.enums import OrderStatusEnum, PaymentStatusEnum
from sqlalchemy import DATE, and_, case, distinct, func, desc, asc
from sqlalchemy.orm import Session
from app.utility.response_utility import apply_filters, apply_pagination
from app.reports.schema.reports_schema import ReportParamSchema
from app.utility.pdf_genration_utility import generate_pdf_response
from app.reports.transformer.reports_transformer import (
    get_dashboard_stats_transformer, dashboard_revenue_transformer, dashboard_orders_transformer,
    customer_stats_transformer, recent_orders_transformer
)

def get_dashboard_stats_service(db: Session):

    start_day = datetime.combine(date.today(), time.min)
    next_day = start_day + timedelta(days=1)

    orders = db.query(
        func.count(Order.id).label("total_orders"),
        func.count(
            case((and_(Order.created_at >= start_day, Order.created_at < next_day), 1))
        ).label("todays_orders"),
        func.count(
            case(
                (
                    ~Order.status.in_(
                        [OrderStatusEnum.COMPLETED, OrderStatusEnum.CANCELLED]
                    ),
                    1,
                )
            )
        ).label("active_orders"),
        func.count(case((Order.status == OrderStatusEnum.COMPLETED, 1))).label(
            "completed_orders"
        ),
        func.count(case((Order.status == OrderStatusEnum.CANCELLED, 1))).label(
            "cancelled_orders"
        ),
    ).one()

    revenue = db.query(
        func.coalesce(
            func.sum(
                case(
                    (
                        and_(
                            Payment.status == PaymentStatusEnum.SUCCESS,
                            Payment.created_at >= start_day,
                            Payment.created_at < next_day,
                        ),
                        Payment.amount,
                    ),
                    else_=0,
                )
            ),
            0,
        ).label("todays_revenue"),
        func.coalesce(
            func.sum(
                case(
                    (Payment.status == PaymentStatusEnum.SUCCESS, Payment.amount),
                    else_=0,
                )
            ),
            0,
        ).label("total_revenue"),
    ).one()

    total_customers = (
        db.query(func.count(User.id))
        .join(UserRole, UserRole.user_id == User.id)
        .filter(User.is_active.is_(True), UserRole.role_id == 1)
        .scalar()
    )
    todays_menu_items = (
        db.query(func.count(DailyMenu.id))
        .filter(DailyMenu.menu_date == date.today())
        .scalar()
    )
    response_data = get_dashboard_stats_transformer(
        orders, revenue, total_customers, todays_menu_items
    )
    return response_data


def dashboard_revenue_service(db: Session, params: ReportParamSchema):
    revenue = db.query(
        func.sum(Payment.amount).label("total_revenue"),
        func.count(Payment.id).label("total_transactions"),
        func.avg(Payment.amount).label("average_order_value"),
    )
    revenue = apply_filters(body=params, model=Payment, query=revenue)
    revenue = revenue.filter(Payment.status == PaymentStatusEnum.SUCCESS).one_or_none()

    revenue_by_date = db.query(
        func.date(Payment.created_at).label("r_date"),
        func.sum(Payment.amount).label("revenue"),
        func.count(Payment.id).label("transactions"),
    )
    revenue_by_date = apply_filters(body=params, model=Payment, query=revenue_by_date)
    revenue_by_date = (
        revenue_by_date.filter(Payment.status == PaymentStatusEnum.SUCCESS)
        .group_by(func.date(Payment.created_at))
        .order_by(func.date(Payment.created_at).desc())
        .all()
    )
    response_data = dashboard_revenue_transformer(params, revenue, revenue_by_date)
    if params.pdf:
        return generate_pdf_response(
            template_name="dashboard_revenue.html",
            data=response_data,
            filename="dashboard_revenue_report.pdf"
        )
    return response_data


def dashboard_orders_service(db: Session, params: ReportParamSchema):
    summery = db.query(
        func.count(Order.id).label("total_orders"),
        func.count(Order.status).filter(Order.status == OrderStatusEnum.PENDING).label("pending"),
        func.count(Order.status).filter(Order.status == OrderStatusEnum.PREPARING).label("preparing"),
        func.count(Order.status).filter(Order.status == OrderStatusEnum.READY).label("ready"),
        func.count(Order.status).filter(Order.status == OrderStatusEnum.COMPLETED).label("completed"),
        func.count(Order.status).filter(Order.status == OrderStatusEnum.CANCELLED).label("cancelled"),
    )
    summery = apply_filters(body=params, model=Order, query=summery)
    summery = summery.one_or_none()

    order_trend = db.query(
        func.date(Order.created_at).label("t_date"),
        func.count(Order.id).label("orders"),
    )
    order_trend = apply_filters(body=params, model=Order, query=order_trend)
    order_trend = (
        order_trend.group_by(func.date(Order.created_at))
        .order_by(func.date(Order.created_at).desc())
        .all()
    )
    response_data = dashboard_orders_transformer(params, summery, order_trend)
    if params.pdf:
            return generate_pdf_response(
                template_name="dashboard_orders.html",
                data=response_data,
                filename="dashboard_orders_report.pdf"
            )
    return response_data


def customer_stats_service(db: Session, params: ReportParamSchema):
    sub_query = db.query(Order.user_id).distinct()
    total_cust_expr = func.count(distinct(User.id)) * 1.0
    summary = db.query(
        func.count(distinct(User.id)).label('total_customers'),
        func.count(distinct(case((User.is_active == True, User.id)))).label('active_customers'),
        func.count(distinct(Order.user_id)).label('customer_with_orders'),
        func.count(case((User.id.notin_(sub_query), 1))).label('customer_wout_orders'),
        func.count(Order.id).label('total_orders'),
        (func.count(Order.id) * 1.0 / func.nullif(total_cust_expr, 0)).label('avg_orders'),
        func.sum(Order.total_amount).label('total_spendings')
    ).outerjoin(Order, User.id == Order.user_id)
    
    top_customers = (
        db.query(
            User.id.label("id"),
            User.name.label("name"),
            func.count(Order.id).label("total_orders"),
            func.sum(Order.total_amount).label("total_spent"),
        )
        .outerjoin(Order, User.id == Order.user_id)
        .group_by(User.id, User.name)
        .order_by(desc("total_orders"))
    )

    customer_growth = (
        db.query(
            func.to_char(User.created_at, 'YYYY-MM').label("period"),
            func.count(User.id).label("new_customers")
        )
        .group_by(func.to_char(User.created_at, 'YYYY-MM'))
        .order_by(desc("period"))
    )
    
    summary = apply_filters(body=params, model= User, query=summary)
    top_customers = apply_filters(body=params, model=User, query=top_customers)
    customer_growth = apply_filters(body=params, model=User, query=customer_growth)
    
    try:
        summary = summary.first()
        top_customers = top_customers.limit(10)
        customer_growth = customer_growth.all()
        response_data = customer_stats_transformer(params, summary, top_customers, customer_growth)
        
        if params.pdf:
            return generate_pdf_response(
                template_name="customer_stats.html",
                data=response_data,
                filename="customer_stats_report.pdf"
            )
        return response_data
    except Exception as e:
        return str(e)
    
    
def recent_orders_service(db:Session, params):
    query = (
        db.query(
            Order.id.label("order_id"),
            Order.user_id.label("customer_id"),
            Order.total_items.label("item_count"),
            Order.total_amount,
            Order.status.label("status"),
            Order.created_at,
            User.name.label("customer_name")
        ).join(
            User, Order.user_id == User.id
        )
    )
    query = apply_filters(body=params, model=Order, query=query)
    query = query.order_by(Order.created_at.desc())
    query, pagination = apply_pagination(body=params, query=query)
    
    response_data = recent_orders_transformer(query.all(), pagination)
    return response_data

