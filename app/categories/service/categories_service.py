from sqlalchemy import and_
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.common_models import Category
from sqlalchemy.exc import IntegrityError
from app.categories.transformer.categories_transformer import (
    get_categories_transformer, get_category_id_transformer
)

def post_category_service(body, db:Session):
    try:
        data = Category(**body.model_dump())
        db.add(data)
        db.commit()
        return True
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                            detail="CATEGORY EXISTS")
    except Exception as e:
        raise HTTPException(status_code=status.WS_1011_INTERNAL_ERROR,
                            detail=f"{e}")
    
    
def get_categories_service(db):
    data = (db.query(Category)
            .filter(Category.is_active == True)
            .all())
    response = get_categories_transformer(data)
    return response

def get_category_id_service(id,db):
    data = (db.query(Category)
            .filter(and_(Category.id == id,
                         Category.is_active == True))
            .first())
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="CATEGORY NOT FOUND")
    response = get_category_id_transformer(data)
    return response

def put_category_id_service(id,body,db):
    data=(db.query(Category)
          .filter(and_(Category.id == id,
                       Category.is_active == True))
          .first())
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="CATEGORY NOT FOUND")
    for k,v in body.model_dump().items():
        setattr(data,k,v)
    db.commit()
    return True    
    
    
def delete_category_id_service(id,db):
    data = (db.query(Category)
            .filter(and_(Category.id == id,
                         Category.is_active == True))
            .first())
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="CATEGORY NOT FOUND")
    data.is_active = False
    db.commit()
    return True