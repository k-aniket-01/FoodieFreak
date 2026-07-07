from sqlalchemy import and_
from app.models.common_models import FoodItem, Category
from psycopg2.errors import ForeignKeyViolation, UniqueViolation
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException,status
from app.food_items.transformer.food_items_transformer import (
    get_food_items_transformer, get_food_item_id_transformer
)

def post_food_items_service(body,db):
    try:
        data = body.model_dump()
        db.add(FoodItem(**data))
        db.commit()
        return True
    except IntegrityError as e:
        db.rollback()
        if isinstance(e.orig, ForeignKeyViolation):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                                detail='CATEGORY DOES NOT EXIST')
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                                detail='ITEM ALREADY EXISTS')
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail=f'SOMETHING WENT WRONG {e}')
    
    
def get_food_items_service(db):
    data = (db.query(FoodItem)
            .join(Category, FoodItem.category_id == Category.id)
            .filter(and_(Category.is_active == True,
                         FoodItem.is_active == True))
            .all())
    response = get_food_items_transformer(data)
    return response


def get_food_item_id_service(id, db):
    data = (db.query(FoodItem)
            .join(Category, FoodItem.category_id == Category.id)
            .filter(and_(FoodItem.id == id,
                         FoodItem.is_active == True,
                         Category.is_active == True))
            .first())
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail='ITEM NOT FOUND')
    response = get_food_item_id_transformer(data)
    return response


def put_food_item_id_service(id,body,db):
    try:
        data = (db.query(FoodItem)
                .join(Category, FoodItem.category_id == Category.id)
                .filter(and_(FoodItem.id == id,
                            FoodItem.is_active == True,
                            Category.is_active == True))
                .first())
        for k,v in body.model_dump().items():
            setattr(data,k,v)
        db.commit()
        return True
    except IntegrityError as e:
        db.rollback()
        if isinstance(e.orig, ForeignKeyViolation):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                                detail='CATEGORY DOES NOT EXIST')
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                            detail='NAME ALREADY EXISTS')
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f'{e}')
    
    
def delete_food_item_service(id,db):
    data = (db.query(FoodItem)
            .join(Category, FoodItem.category_id == Category.id)
            .filter(and_(FoodItem.id ==id,
                         FoodItem.is_active == True,
                         Category.is_active == True))
            .first())
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='ITEM DOES NOT EXIST')
    data.is_active = False
    db.commit()
    return True
    
def patch_food_availability_service(id, body, db):
    data = (db.query(FoodItem)
            .join(Category, FoodItem.category_id == Category.id)
            .filter(and_(FoodItem.id == id,
                         FoodItem.is_active == True,
                         Category.is_active == True))
            .first())
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='ITEM DOES NOT EXIST')
    for k,v in body.model_dump().items():
        setattr(data,k,v)
    db.commit()
    return True,
           