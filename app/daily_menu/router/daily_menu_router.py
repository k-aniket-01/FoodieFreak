from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.utility.auth_utility import require_owner, get_db
from app.daily_menu.schema.daily_menu_schema import  DailyMenuRequestSchema
from app.daily_menu.service.daily_menu_service import post_daily_menu_service


daily_menu_router = APIRouter()


@daily_menu_router.post('/post/batch/daily/menu')
def post_daily_menu(body:DailyMenuRequestSchema,
                    db: Session = Depends(get_db),
                    user = Depends (require_owner)
                    ):
    response_data = post_daily_menu_service(body,db)
    return response_data