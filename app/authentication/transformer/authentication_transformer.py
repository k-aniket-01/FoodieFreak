from app.authentication.schema.authentication_schema import (
    AuthRegisterResponseSchema, AuthLoginResponseSchema, AuthMeResponseSchema
)


def auth_register_transformer(data):
    response = (AuthRegisterResponseSchema
                .model_validate(data, from_attributes=True)
                .model_dump())
    return response
    
    
def auth_login_transformer(data):
    response = (AuthLoginResponseSchema
                .model_validate(data, from_attributes=True)
                .model_dump())
    return response 

def auth_me_transformer(data):
    response = (AuthMeResponseSchema
                .model_validate(data, from_attributes=True)
                .model_dump())
    return response
