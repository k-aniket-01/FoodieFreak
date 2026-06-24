from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from app.models.common_models import *
import os

load_dotenv()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30    


pwd_context = CryptContext(
    schemes=['bcrypt'],
    deprecated = 'auto'
)

def hash_password(password:str):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def create_jwt_token(data:dict, expires_minutes:int = ACCESS_TOKEN_EXPIRE_MINUTES):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

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
    
    email = payload.get("sub")
    if email is None:
        raise cred_exception
    
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise cred_exception
    return user
