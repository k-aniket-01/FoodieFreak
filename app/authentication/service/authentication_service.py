import os 
import time
from dotenv import load_dotenv
from datetime import date
import secrets
from jinja2 import Template
from fastapi_mail import  MessageSchema, MessageType
from app.utility.mail_utility import fast_mail, forgot_password_template
from app.utility.auth_utility import  REFRESH_TOKEN_EXPIRE_DAYS
from sqlalchemy import  and_
from app.models.common_models import User, UserRole
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from app.database import redis_cache
from app.utility.auth_utility import (
    hash_password, verify_password, create_access_token, create_refresh_token, decode_token
)
from app.authentication.schema.authentication_schema import (
    AuthRegisterRequestSchema, AuthLoginRequestSchema, AuthUpdatePassRequestSchema
)
from app.authentication.transformer.authentication_transformer import (
    auth_register_transformer , auth_login_transformer, auth_me_transformer
)

load_dotenv()
    
def auth_register_service(data:AuthRegisterRequestSchema, db: Session):  
    data.password = hash_password(data.password)
    
    try:
        user_data = data.model_dump(exclude={"confirm_password", "role"})
        new_user = User(**user_data)
        db.add(new_user)
        db.flush()
        userrole = UserRole(user_id = new_user.id, role_id = data.role )
        db.add(userrole)
        db.commit()
        response_data = auth_register_transformer(new_user)
        return response_data
    except IntegrityError:      
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="EMAIL/PHONE ALREADY EXISTS")
    except Exception as e:  
        raise HTTPException(e)
    
    
def auth_login_service(data:AuthLoginRequestSchema, db:Session):
    user = (
        db.query(User).filter(
            and_( User.email == data.email, User.is_active == True)
            )).first()
    if user:
        verified = verify_password(data.password, user.password)
        if verified:
            access_token, _ = create_access_token(data={"sub":str(user.id)})
            refresh_token,_ = create_refresh_token(data={"sub":str(user.id)})
            data = {
                "token_type" : "Bearer",
                "access_token" : access_token,
                "refresh_token" : refresh_token,
            }
            # redis_cache.setex(f"refresh:{refresh_jti}",timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS), user.id)
            response = auth_login_transformer(data)
            return response
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="WRONG CREDENTIALS")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="USER NOT FOUND")            
        
        
def auth_refresh_service(body,db):
    payload = decode_token(body.refresh_token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail='INVALID TOKEN')
    if payload['type'] != 'refresh' :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='INVALID TOKEN TYPE')
        
    blacklist = redis_cache.get(f"blacklist:{payload['jti']}")
    if blacklist == str(payload['sub']):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='INVALID TOKEN OR BLACKLISTED')

    user = db.query(User).filter( User.id == payload.get("sub"), User.is_active == True).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="INVALID USER")
    access_token, _ = create_access_token(data={"sub":str(user.id)})
    refresh_token,_ = create_refresh_token(data={"sub":str(user.id)})
    data = {
        "token_type" : "Bearer",
        "access_token" : access_token,
        "refresh_token" : refresh_token,
    }
    # redis_cache.setex(f"refresh:{refresh_jti}",timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS), user.id)
    response = auth_login_transformer(data)
    return response
    
def auth_update_pwd_service(data:AuthUpdatePassRequestSchema, user, db:Session):
    verified = verify_password(data.current_password, user.password)
    if verified:
        is_same = verify_password(data.confirm_password, user.password)
        if is_same:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, 
                                detail="CURRENT PASSWORD & NEW PASSWORD CANNOT BE SAME")
        user.password = hash_password(data.new_password)
        db.commit()
        return True
    else:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                            detail="WRONG CREDENTIALS")
            
            
def auth_me_service(data):
    response = auth_me_transformer(data)
    return response


def auth_logout_service(body,user):
    payload = decode_token(body.refresh_token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='INVALID TOKEN')
    ttl = payload['exp'] - int(time.time())
    if payload["type"] != 'refresh':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='INVALID TOKEN TYPE')
    if user.id != int(payload['sub']):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='INVALID TOKEN')
    redis_cache.setex(f"blacklist:{payload['jti']}", ttl , user.id)
    return True
    
    
async def auth_forgot_password_service(body,db):
    email = body.email
    user = db.query(User).filter(User.email == email, User.is_active == True).first()
    template = Template(forgot_password_template)
    if user is not None:
        token = secrets.token_urlsafe(50)
        html = template.render(
                name=user.name,
                reset_link =f"{os.getenv('FoodieFreakUrl')}/reset/password?token={token}",
                year=date.today().year
                )
        message = MessageSchema(
            subject='Rest Your FoodieFreak Account - FoodieFreak',
            recipients= [email],
            body = html,
            subtype= MessageType.html
        )
        await fast_mail.send_message(message)
        redis_cache.setex(f"reset_token:{token}",300,user.email)
        return  True
    return True
    
def auth_reset_password_service(token, body, db):
    email = redis_cache.getdel(f"reset_token:{token}")
    print(email)
    if email is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail='INVALID TOKEN')
    user = db.query(User).filter(User.email == email, User.is_active == True).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                detail='INVALID TOKEN')
    hash = hash_password(body.password)
    user.password = hash 
    try:
        db.commit()
        return True
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"{e}")