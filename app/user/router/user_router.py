from fastapi import APIRouter, Depends
from app.utility.auth_utility import get_current_user, get_db
from app.user.service.user_service import get_user_profile_service

user_router = APIRouter()


@user_router.get('/user/profile')
def get_user_profile(user=Depends(get_current_user)):
    data = get_user_profile_service(user)
    return data 