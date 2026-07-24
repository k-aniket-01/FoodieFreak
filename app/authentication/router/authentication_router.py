from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.utility.auth_utility import get_current_user
from app.authentication.schema.authentication_schema import (
    AuthRegisterRequestSchema, AuthLoginRequestSchema, AuthUpdatePassRequestSchema,
    
)
from app.authentication.service.authentication_service import (
    auth_register_service, auth_login_service, auth_update_pwd_service, 
    auth_me_service, auth_refresh_service
)

auth_router = APIRouter()


@auth_router.post('/auth/register')
def auth_registration(body:AuthRegisterRequestSchema, db:Session=Depends(get_db)):
    response = auth_register_service(body, db)
    return  response 


#keep for swagger login (jwt header issue solver)
@auth_router.post('/auth/login')
async def auth_login(request : Request, db:Session=Depends(get_db)):
    form = await request.form()
    data = AuthLoginRequestSchema(email=form["username"], password=form["password"])
    response = auth_login_service(data, db)
    return response


@auth_router.post('/login')
def auth_login(body:AuthLoginRequestSchema, db:Session=Depends(get_db)):
    response = auth_login_service(body, db)
    return response 


@auth_router.post('/auth/refresh')
def auth_refresh(token:str, db:Session=Depends(get_db)):
    response = auth_refresh_service(token,db)
    return response




@auth_router.patch('/update/password')
def auth_update_password(body:AuthUpdatePassRequestSchema,
                         user=Depends(get_current_user),
                         db:Session=Depends(get_db)):
    response = auth_update_pwd_service(body, user, db)
    return response


@auth_router.get('/auth/me')
def auth_me(user=Depends(get_current_user)):
    response = auth_me_service(user)
    return response

