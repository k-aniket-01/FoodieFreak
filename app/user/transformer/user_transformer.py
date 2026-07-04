from app.user.schema.user_schema import (
    UserProfileResponseSchema, UserProfileUpdateResponseSchema, GetUserOrdersSchema,
    GetUserPaymentsSchema
)

def get_user_profile_transformer(data):
    response = (UserProfileResponseSchema
            .model_validate(data, from_attributes=True)
            .model_dump())
    return response

def update_user_profile_transformer(data):
    response = (UserProfileUpdateResponseSchema
            .model_validate(data, from_attributes=True)
            .model_dump())
    return response

def get_user_orders_transformer(data):
    response = (GetUserOrdersSchema
                .model_validate(data, from_attributes=True)
                .model_dump())
    return response

def get_user_payments_transformer(query):
    response = (GetUserPaymentsSchema
                .model_validate(data, from_attributes=True)
                .model_dump()for data in query)
    return response