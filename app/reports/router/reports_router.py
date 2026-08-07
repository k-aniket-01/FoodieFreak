from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.utility.auth_utility import require_owner 
from app.reports.schema.reports_schema import ReportParamSchema
from app.reports.service.reports_service import (
    get_dashboard_stats_service, dashboard_revenue_service, dashboard_orders_service
)

reports_router = APIRouter()


@reports_router.get('/dashboard/stats', dependencies=[Depends(require_owner)])
def get_dashboard_stats(db:Session=Depends(get_db)):
    response_data = get_dashboard_stats_service(db)
    return response_data

@reports_router.get('/dashboard/revenue', dependencies=[Depends(require_owner)])
def get_dashboard_revenue(db:Session=Depends(get_db), params: ReportParamSchema=Depends()):
    resposne_data = dashboard_revenue_service(db, params)
    return resposne_data 

@reports_router.get('/dashboard/orders', dependencies=[Depends(require_owner)])
def get_dashboard_orders(
        db:Session=Depends(get_db), 
        params: ReportParamSchema=Depends()
    ):
    response_data = dashboard_orders_service(db, params)
    return response_data
