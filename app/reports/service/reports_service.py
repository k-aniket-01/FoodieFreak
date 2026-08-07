from datetime import date, datetime, time, timedelta
from app.models.common_models import DailyMenu, Order, Payment, User, UserRole
from app.utility.enums import OrderStatusEnum, PaymentStatusEnum
from sqlalchemy import DATE, and_, case, func
from sqlalchemy.orm import Session
from app.utility.response_utility import apply_filters
from app.reports.schema.reports_schema import DashboardRevenueParamSchema
from app.utility.pdf_genration_utility import generate_pdf_response
from app.reports.transformer.reports_transformer import (
    get_dashboard_stats_transformer, dashboard_revenue_transformer
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
        ).label("total_revenue")).one()

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
        orders, 
        revenue, 
        total_customers, 
        todays_menu_items
        )
    return response_data


def dashboard_revenue_service(db: Session, params: DashboardRevenueParamSchema):
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
