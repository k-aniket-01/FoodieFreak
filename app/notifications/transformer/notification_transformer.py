from app.notifications.schema.notification_schema import GetNotificationResponseSchema


def get_notification_transformer(data):
    response_data = (
        GetNotificationResponseSchema
        .model_validate(item, from_attributes=True)
        .model_dump()
        for item in data
    )
    return response_data
