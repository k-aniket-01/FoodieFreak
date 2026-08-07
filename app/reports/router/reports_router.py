from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.utility.auth_utility import require_owner 
from app.reports.service.reports_service import get_dashboard_stats_service


reports_router = APIRouter()


@reports_router.get('/dashboard/stats')
def get_dashboard_stats(db:Session=Depends(get_db), user=Depends(require_owner)):
    response_data = get_dashboard_stats_service(db, user)
    return response_data

