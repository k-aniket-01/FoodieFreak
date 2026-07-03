from app.authentication.schema.authentication_schema import (
    AuthRegisterResponseSchema, AuthLoginResponseSchema
)


def auth_register_transformer(data):
    data = (AuthRegisterResponseSchema.model_validate(data, from_attributes=True)).model_dump()
    return data
    
    
def auth_login_transformer(data):
    data = (AuthLoginResponseSchema.model_validate(data, from_attributes=True)).model_dump()
    return data 

