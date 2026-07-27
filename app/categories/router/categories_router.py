from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.utility.auth_utility import require_owner
from app.categories.schema.categories_schema import (
    PostCategoriesRequestSchema, PutCategoryIdSchema
)
from app.categories.service.categories_service import (
    post_category_service, get_categories_service, get_category_id_service, 
    put_category_id_service, delete_category_id_service, 
)

categories_router = APIRouter()

@categories_router.post('/post/category')
def post_category(body:PostCategoriesRequestSchema,
                  user=Depends(require_owner),
                  db:Session=Depends(get_db),
                  ):
    response = post_category_service(body, db)
    return response 

@categories_router.get('/get/categories')
def get_categories(db:Session= Depends(get_db)
                   ):
    response = get_categories_service(db)
    return response

@categories_router.get('/get/category/{id:int}')
def get_category_id(id:int,
                    db:Session=Depends(get_db)
                     ):
    response = get_category_id_service(id,db)
    return response

@categories_router.put('/put/category/{id:int}')
def put_category_id(id:int,body:PutCategoryIdSchema,
                    db:Session=Depends(get_db),
                    user=Depends(require_owner)
                    ):
    response = put_category_id_service(id,body,db)
    return response

@categories_router.delete('/delete/category/{id:int}')
def delete_category_id(id:int,
                       db:Session=Depends(get_db),
                       user=Depends(require_owner)
                       ):
    response = delete_category_id_service(id,db)
    return response