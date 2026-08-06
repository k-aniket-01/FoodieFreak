from app.models.common_models import Notification
from app.notifications.transformer.notification_transformer import (
    get_notification_transformer,
)
from fastapi import HTTPException, status


async def create_notification_service(db, user_id: int, title: str, message: str):
    notification = db.add(Notification(user_id=user_id, title=title, message=message))
    db.add(notification)
    await db.flush()
    return notification


def get_notification_service(db, user):
    query = db.query(Notification).filter(Notification.user_id == user.id).all()
    response_data = get_notification_transformer(query)
    return response_data


def unread_notification_service(db, user):
    query = (
        db.query(Notification)
        .filter(Notification.user_id == user.id, Notification.is_read == False)
        .order_by(Notification.created_at)
        .desc()
        .all()
    )
    response_data = get_notification_transformer(query)
    return response_data


def read_notification_service(id, db, user):
    query = (
        db.query(Notification)
        .filter(Notification.user_id == user.id, Notification.id == id)
        .first()
    )
    if not query:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="NOTIFICATION NOT FOUND"
        )
    try:
        query.is_read = True
        db.commit()
        return True
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}"
        )


def read_all_notification_service(db, user):
    query = (
        db.query(Notification)
        .filter(Notification.user_id == user.id, Notification.is_read == False)
        .all()
    )
    if not query:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="NOTIFICATION NOT FOUND"
        )
    try:
        for notification in query:
            notification.is_read = True
        db.commit()
        return {"status":True, "message":f"All {len(query)} notifications marked as read."}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}"
        )
        
        
def delete_notification_service(id, db, user):
    query = (
        db.query(Notification)
        .filter(Notification.user_id == user.id, Notification.id == id)
        .first()
    )
    if not query:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="NOTIFICATION NOT FOUND"
        )
    try:
        db.delete(query)
        db.commit()
        return True
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}"
        )