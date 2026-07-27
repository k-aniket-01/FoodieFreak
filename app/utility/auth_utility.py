from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.database import get_db
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from app.models.common_models import *
import os
import uuid

load_dotenv()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15   
REFRESH_TOKEN_EXPIRE_DAYS = 2


pwd_context = CryptContext(
    schemes=['bcrypt'],
    deprecated = 'auto'
)

def hash_password(password:str):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def create_access_token(data:dict, expires_minutes:int = ACCESS_TOKEN_EXPIRE_MINUTES):
    to_encode = data.copy()
    jti = str(uuid.uuid4())
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    to_encode.update({"exp":expire})
    to_encode["type"] = "access"
    to_encode["jti"] = jti 
    access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return access_token, jti

def create_refresh_token(data:dict, expires_days:int=REFRESH_TOKEN_EXPIRE_DAYS):
    to_encode = data.copy()
    jti = str(uuid.uuid4())
    expire = datetime.now(timezone.utc) + timedelta(days=expires_days)
    to_encode.update({"exp":expire})
    to_encode["type"] = "refresh"
    to_encode["jti"] = jti
    refresh_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return refresh_token, jti

def decode_token(token:str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None
    

def get_current_user(token:str =Depends(oauth2_scheme), db:Session=Depends(get_db)):
    cred_exception = HTTPException(
        status_code=401,
        detail='Invalid token',
        headers={'WWW-Authenticate':'Bearer'}
    )
    payload = decode_token(token)
    if payload is None:
        raise cred_exception
    user_id = int(payload.get("sub"))
    if user_id is None:
        raise cred_exception
    user = db.query(User).filter(and_(User.id == user_id, User.is_active == True)).first()
    if user is None:
        raise cred_exception
    return user

def require_role(role_name:str):
    def role_checker(current_user : User =  Depends(get_current_user)):
        user_roles = [role.name for role in current_user.roles]
        if role_name not in user_roles:
            raise HTTPException(
                status_code=403,
                detail="Permission Denied"
            )
        return current_user
    return role_checker

require_customer = require_role("CUSTOMER")
require_owner = require_role("CANTEEN_OWNER")