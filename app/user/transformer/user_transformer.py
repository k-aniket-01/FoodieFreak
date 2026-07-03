from app.user.schema.user_schema import UserProfileResponseSchema
def get_user_profile_transformer(data):
    data = UserProfileResponseSchema.model_validate(data, from_attributes=True).model_dump()
    return data