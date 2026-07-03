from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.utility.auth_utility import get_current_user
from app.authentication.schema.authentication_schema import (
    AuthRegisterRequestSchema, AuthLoginRequestSchema, AuthUpdatePassRequestSchema
)
from app.authentication.service.authentication_service import (
    auth_register_service, auth_login_service, auth_update_pwd_service
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

@auth_router.patch('/update/password')
def auth_update_password(body:AuthUpdatePassRequestSchema,
                         user=Depends(get_current_user),
                         db:Session=Depends(get_db)):
    response = auth_update_pwd_service(body, user, db)
    return response














# def login(data:LoginRequest, db:Session=Depends(get_db)):
#     user = db.query(User).filter(User.email == data.email).first()
#     if not user:
#         return {"status":False, "message":"User not Found"}
#     if user.is_deleted:
#         return {"status":False, "message":"User not Found"}
#     if not verify_password(data.password, user.password_hash):
#         return {"status":False, "message":"Invalid Credentials"}
#     access_token = create_jwt_token(data={"sub":user.email})
    
#     return {
#         "access_token":access_token,
#         "type":"bearer"
#         }

# @router.get('/auth/me', response_model=AuthMeResponse)
# def auth_me(current_user:User=Depends(get_current_user)):
#     return current_user

# @router.get('/test/customer') #test purpose  route delete later
# def rabc_customer(current_user: User = Depends(require_customer)):
#     return "yes its customer"

# @router.get('/test/owner') #test purpose route delete later
# def rabc_owner(current_user: User = Depends(require_owner)):
#     return "yes its owner"

# @router.patch('/auth/update-password')
# def update_password(
#     data:UpdatePassSchema,
#     User = Depends(get_current_user),
#     db: Session=Depends(get_db)):
#     valid = verify_password(data.current_pass, User.password_hash)
#     if not valid:
#         return {
#                 "status": False,
#                 "message":"Password invalid"
#                 }
#     is_same = pwd_context.verify(data.current_pass, User.password_hash)
#     if is_same:
#         return {
#                 "status": False,
#                 "message": "New password must be different from current password"
#                 }
#     new_pass = hash_password(data.new_pass)
#     User.password_hash = new_pass
#     db.commit()
#     return {
#             "status": True,
#             "message":"Password update successful"
#             }
