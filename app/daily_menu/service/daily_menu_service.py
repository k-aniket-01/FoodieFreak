from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
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