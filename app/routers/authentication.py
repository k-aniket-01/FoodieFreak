from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.auth_schema import *
from app.models.common_models import *
from app.services.auth_services import *

router = APIRouter()

@router.get('/')
def home():
    return {"status":True,
            "message":"welocme dev"}

@router.post('/auth/register')
def registration(data:RegisterRequest, db:Session=Depends(get_db)):
    email = db.query(User).filter(User.email == data.email).first()
    if email:
        return {"status":False, "message":"Email already exists"}
    
    phone = db.query(User).filter(User.phone == data.phone).first()
    if phone:
        return {"status":False, "message":"Phone already exists"}
    
    role = db.query(Role).filter(Role.name == data.role).first()
    print(data.role)
    if not role:
        return {"status":False, "message":"Role not Found"}
    
    hashed_password = hash_password(data.password)

    new_user = User(
        name=data.name,
        email=data.email,
        phone=data.phone,
        password_hash = hashed_password
    )
    db.add(new_user)
    db.flush()

    user_role = UserRole(user_id = new_user.id,role_id = role.id)
    db.add(user_role)
    db.commit()

    return {
        "status":True,
        "message":"Registration sucessful",
        "user_id":new_user.id
    }