# from pydantic import BaseModel
# from typing import Optional, Any
# # from app.schemas.auth_schema import RoleSchema, OrderSchema

# class UserPofileSchema(BaseModel):
#     id : Optional[int] = None
#     name : Optional[str] = None 
#     email : Optional[str] = None                         
#     phone : Optional[str] = None               
#     created_at : Optional[Any] = []   
#     # roles : Optional[list[RoleSchema]] = []
#     # carts : Optional[list[Any]] = []
#     # orders : Optional[list[OrderSchema]] = [] 

#     class config:
#         from_attributes = True

# class UpdateUserSchema(BaseModel):
#     name : Optional[str]
#     phone : Optional[str]

# class UserOrdersResponseSchema(BaseModel):
#     name : Optional[Any] = None
#     id : Optional[Any] = None
#     total_amount : Optional[Any] = None
#     status : Optional[Any] = None