from app.user.schema.user_schema import UserProfileResponseSchema, UserProfileUpdateResponseSchema


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

