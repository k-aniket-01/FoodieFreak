# from fastapi import APIRouter, Depends
# from app.models.common_models import *
# from app.schemas.user_schema import *
# # from app.services.auth_services import *
# from app.utility.auth_utility import get_current_user, get_db
# from sqlalchemy.orm import Session
# from fastapi import APIRouter, Depends, Request
# from sqlalchemy.orm import Session
# from app.database import get_db
# from app.authentication.schema.authentication_schema import (
#     AuthRegisterRequestSchema, AuthLoginRequestSchema
# )
# from app.authentication.service.authentication_service import (
#     auth_register_service, auth_login_service
# )


# router = APIRouter()

# # @router.get('/user/profile', response_model=UserPofileSchema)
# # def user_profile(
# #     data : User=Depends(get_current_user)
# #                 ):
# #     return data

# @router.put('/update/user')
# def update_user(
#     data,
#     user = Depends(get_current_user),
#     db : Session = Depends(get_db) 
# ):
#     print("User Request recieved")
#     values = dict(data)
#     db.query(User).filter(User.id == user.id).update(values)
#     db.commit()
#     db.refresh(user)
#     return user 


# # @router.delete('/delete/user')
# # def delete_user(
# #     user = Depends(get_current_user),
# #     db : Session = Depends(get_db)
# # ):
# #     db.query(User).filter(User.id==user.id).update({"is_deleted":True})
# #     db.commit()
# #     db.refresh(user)
# #     return user

# # @router.get('/user/orders/', response_model=list[UserOrdersResponseSchema])
# # def get_user_orders(
# #     db:Session=Depends(get_db), 
# #     user : User = Depends(get_current_user)
# # ):
# #     query = (
# #         db.query(
# #             User.name, 
# #             Order.id,
# #             Order.total_amount,
# #             Order.status
# #             )
# #         .join(Order, User.id == Order.user_id)
# #         .filter(User.id == user.id)
# #         .all()
# #              )
# #     return query