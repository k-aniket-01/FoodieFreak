from sqlalchemy import or_, and_
from app.models.common_models import User, UserRole
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from app.utility.auth_utility import (
    hash_password, verify_password, create_jwt_token, get_current_user
)
from app.authentication.schema.authentication_schema import (
    AuthRegisterRequestSchema, AuthLoginRequestSchema, AuthUpdatePassRequestSchema
)
from app.authentication.transformer.authentication_transformer import (
    auth_register_transformer , auth_login_transformer
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
            and_( User.email == data.email, User.is_deleted != True)
            )).first()
    if user:
        verified = verify_password(data.password, user.password)
        if verified:
            data = {
                "access_token" :create_jwt_token(data={"sub":user.email}),
                "token_type" : "Bearer"
            }
            response = auth_login_transformer(data)
            return response
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="WRONG CREDENTIALS")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="USER NOT FOUND")            
        
        
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
            