from fastapi import APIRouter, Depends
from app.database import get_db
from app.utility.auth_utility import get_current_user
from sqlalchemy.orm import Session
from app.notifications.service.notification_service import (
    get_notification_service, unread_notification_service, read_notification_service,
    read_all_notification_service, delete_notification_service
)

notification_router = APIRouter()


@notification_router.get('/notification/get')
def get_notification(
        db:Session=Depends(get_db),
        user=Depends(get_current_user)
    ):
    response_data = get_notification_service(db, user)
    return response_data


@notification_router.get('/notification/unread')
def unread_notification(
        db:Session=Depends(get_db),
        user=Depends(get_current_user)
    ):
    response_data = unread_notification_service(db, user)
    return response_data


@notification_router.patch('/notification/{id:int}/read')
def read_notification(
        id:int,          
        db:Session=Depends(get_db),
        user=Depends(get_current_user)
    ):
    response_data = read_notification_service(id, db, user)
    return response_data


@notification_router.patch('/notification/read/all')
def read_all_notification(
        db:Session=Depends(get_db),
        user=Depends(get_current_user)
    ):
    response_data = read_all_notification_service(db, user)
    return response_data


@notification_router.delete('/notification/{id:int}/delete')
def delete_notification(
        id:int,          
        db:Session=Depends(get_db),
        user=Depends(get_current_user)
    ):
    response_data = delete_notification_service(id, db, user)
    return response_data