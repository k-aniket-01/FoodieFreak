from fastapi import APIRouter, Depends
from app.models.common_models import *
from app.schemas.user_schema import *
from app.services.auth_services import *

router = APIRouter()

@router.get('/user/profile', response_model=UserPofileSchema)
def user_profile(
    data : User=Depends(get_current_user)
                ):
    return data

@router.put('/update/user', response_model=UserPofileSchema)
def update_user(
    data: UpdateUserSchema,
    user = Depends(get_current_user),
    db : Session = Depends(get_db) 
):
    values = dict(data)
    db.query(User).filter(User.id == user.id).update(values)
    db.commit()
    db.refresh(user)
    return user 

@router.delete('/delete/user')
def delete_user(
    user = Depends(get_current_user),
    db : Session = Depends(get_db)
):
    db.query(User).filter(User.id==user.id).update({"is_deleted":True})
    db.commit()
    db.refresh(user)
    return user

@router.get('/user/orders/')
def get_user_orders(db:Session=Depends(get_db), user:User= Depends(get_current_user)):
    query = (
        db.query(User, Order)
        .join(Order, User.id == Order.user_id)
        .filter(User.id == user.id)
        .all()
             )
    data = [
        {
            "name":user.name, 
            "order":order.id,
            "amount":order.total_amount,
            "status":order.status
            }
            for user, order in query
            ]
    return data