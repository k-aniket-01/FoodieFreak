from fastapi import HTTPException, status
from datetime import date
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
from app.daily_menu.transformer.daily_menu_transformer import get_daily_menu_transformer
from app.models.common_models import DailyMenu


def post_daily_menu_service(body, db):
    try:
        data = []
        for item in body.food_items:
            data.append(
                DailyMenu(
                    food_item_id =item.food_item_id,
                    menu_date =body.menu_date,
                    available_qty =item.available_qty
                    )
                )
        db.add_all(data)
        db.commit()
        return True
    except IntegrityError as e :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"{e.orig.diag.message_detail}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"{e}")
        

def get_daily_menu_today_service(db):
    dt = date.today()
    data = (db.query(DailyMenu)
            .filter(
                and_(
                    DailyMenu.menu_date == dt,
                    DailyMenu.is_available == True
                    )
                )
            ).all()
    response_data = get_daily_menu_transformer(data)
    return response_data
    
        
def get_daily_menu_service(dt,db):
    data = (db.query(DailyMenu)
             .filter(
                 and_(
                     DailyMenu.menu_date == dt,
                     DailyMenu.is_available == True
                     )
                 )
             ).all()
    response_data = get_daily_menu_transformer(data)
    return response_data


def put_daily_menu_service(id, body, db):
    data = (db.query(DailyMenu)
            .filter(DailyMenu.id == id)
            ).first()
    if data:
        try:
            for k,v in body.model_dump().items():
                setattr(data, k, v)
            db.commit()
            return True
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"{e.orig.diag.message_detail}")
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail=["MENU ITEM NOT FOUND"])
    
    
def delete_daily_menu_item_service(id, db):
    data = (db.query(DailyMenu)
            .filter(DailyMenu.id == id)
            ).first()
    if data:
        db.delete(data)
        db.commit()
        return {"status":True,
                "message":f"Deleted {id}"}
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail=["MENU ITEM NOT FOUND"])
     