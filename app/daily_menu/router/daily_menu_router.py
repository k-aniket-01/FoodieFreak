from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.utility.auth_utility import require_owner, get_db
from app.daily_menu.schema.daily_menu_schema import  DailyMenuRequestSchema, PutDailyMenuRequestSchema
from app.daily_menu.service.daily_menu_service import (
    post_daily_menu_service, get_daily_menu_service, get_daily_menu_today_service,
    put_daily_menu_service, delete_daily_menu_item_service    
)

daily_menu_router = APIRouter()


@daily_menu_router.post('/post/batch/daily/menu')
def post_daily_menu(body:DailyMenuRequestSchema,
                    db: Session = Depends(get_db),
                    user = Depends (require_owner)
                    ):
    response_data = post_daily_menu_service(body, db)
    return response_data


@daily_menu_router.get('/get/daily/menu/today')
def get_daily_menu_today(db:Session=Depends(get_db)
                         ):
    response_data = get_daily_menu_today_service(db)
    return response_data


@daily_menu_router.get('/get/daily/menu/{dt:str}')
def get_daily_menu(dt, db:Session=Depends(get_db)
                   ):
    response_data = get_daily_menu_service(dt, db)
    return response_data


@daily_menu_router.put('/put/daily/menu/{id:int}')
def put_daily_menu(id,
                   body: PutDailyMenuRequestSchema,
                   db:Session = Depends(get_db),
                   user = Depends(require_owner)
                   ):
    response_data = put_daily_menu_service(id, body, db)
    return response_data


@daily_menu_router.delete('/delete/daily/menu/item/{id:int}')
def delete_daily_menu_item(id,
                           db:Session=Depends(get_db),
                           user= Depends(require_owner)
                           ):
    response_data = delete_daily_menu_item_service(id, db)
    return response_data