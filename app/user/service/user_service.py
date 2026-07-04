from sqlalchemy.orm import Session
from app.models.common_models import User, Order, Payment
from app.user.transformer.user_transformer import (
    get_user_profile_transformer, update_user_profile_transformer, get_user_orders_transformer,
    get_user_payments_transformer,
)

def get_user_profile_service(data):
    response = get_user_profile_transformer(data)
    return response

def update_user_profile_service(body, user:User, db):
    data = body.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(user,key, value)
    db.commit()
    db.refresh(user)
    response = update_user_profile_transformer(user)
    return response

def delete_user_profile_service(user:User, db):
    user.is_active = False
    db.commit()
    return True

def get_user_orders_service(user):
    response = get_user_orders_transformer(user)
    return response

def get_user_payment_service(db):
    query = (db.query(User.id,
                      User.name,
                      User.email,
                      User.phone,
                      User.is_active,
                      Payment.order_id,
                      Payment.transaction_id,
                      Payment.payment_method,
                      Payment.status)
             .join(Order, User.id == Order.user_id)
             .join(Payment, Order.id == Payment.order_id))
    query = query.all()
    print(query)
    print(type(query))
    response = get_user_payments_transformer(query)
    
    return response