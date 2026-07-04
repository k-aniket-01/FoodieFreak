from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.utility.auth_utility import get_current_user, get_db
from app.user.schema.user_schema import UserProfileUpdateRequestSchema
from app.user.service.user_service import (
    get_user_profile_service, update_user_profile_service 
)

user_router = APIRouter()


@user_router.get('/get/user/profile')
def get_user_profile(user=Depends(get_current_user)):
    response = get_user_profile_service(user)
    return response 

@user_router.put('/get/user/profile')
def update_user_profile(
        body:UserProfileUpdateRequestSchema,
        user = Depends(get_current_user),
        db:Session = Depends(get_db)
    ):
    response = update_user_profile_service(body, user, db)
    return response
