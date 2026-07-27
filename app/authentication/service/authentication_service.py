from datetime import timedelta
from fastapi import Depends
from app.utility.auth_utility import get_current_user, REFRESH_TOKEN_EXPIRE_DAYS
from sqlalchemy import or_, and_
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
            refresh_token,refresh_jti = create_refresh_token(data={"sub":str(user.id)})
            data = {
                "token_type" : "Bearer",
                "access_token" : access_token,
                "refresh_token" : refresh_token,
            }
            redis_cache.setex(f"refresh:{refresh_jti}",timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS), user.id)
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
        
    stored_email = redis_cache.getdel(f"refresh:{payload['jti']}")
    if stored_email is None or stored_email != payload['sub']:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='INVALID TOKEN')

    user = db.query(User).filter( User.id == payload.get("sub"), User.is_active == True).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="INVALID USER")
    access_token, _ = create_access_token(data={"sub":str(user.id)})
    refresh_token,refresh_jti = create_refresh_token(data={"sub":str(user.id)})
    data = {
        "token_type" : "Bearer",
        "access_token" : access_token,
        "refresh_token" : refresh_token,
    }
    redis_cache.setex(f"refresh:{refresh_jti}",timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS), user.id)
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
    if payload["type"] != 'refresh':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='INVALID TOKEN TYPE')
    if user.id != int(payload['sub']):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='INVALID TOKEN')
    redis_cache.delete(f"refresh:{payload['jti']}")
    return True
    