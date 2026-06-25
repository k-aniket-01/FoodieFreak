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

@router.post('/auth/login')
def login(data:LoginRequest, db:Session=Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        return {"status":False, "message":"User not Found"}
    if not verify_password(data.password, user.password_hash):
        return {"status":False, "message":"Invalid Credentials"}
    access_token = create_jwt_token(data={"sub":user.email})
    
    return {
        "access_token":access_token,
        "type":"bearer"
        }

@router.get('/auth/me', response_model=AuthMeResponse)
def auth_me(current_user:User=Depends(get_current_user)):
    return current_user

@router.get('/test/customer') #test purpose  route delete later
def rabc_customer(current_user: User = Depends(require_customer)):
    return "yes its customer"

@router.get('/test/owner') #test purpose route delete later
def rabc_owner(current_user: User = Depends(require_owner)):
    return "yes its owner"

@router.patch('/auth/update-password')
def update_password(
    data:UpdatePassSchema,
    User = Depends(get_current_user),
    db: Session=Depends(get_db)):
    valid = verify_password(data.current_pass, User.password_hash)
    if not valid:
        return {
                "status": False,
                "message":"Password invalid"
                }
    is_same = pwd_context.verify(data.current_pass, User.password_hash)
    if is_same:
        return {
                "status": False,
                "message": "New password must be different from current password"
                }
    new_pass = hash_password(data.new_pass)
    User.password_hash = new_pass
    db.commit()
    return {
            "status": True,
            "message":"Password update successful"
            }
