from sqlalchemy.orm import Session
from app.models.common_models import User
from app.user.transformer.user_transformer import (
    get_user_profile_transformer, update_user_profile_transformer
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