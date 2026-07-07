from fastapi import FastAPI 
from app.authentication.router.authentication_router import auth_router
from app.user.router.user_router import user_router
from app.categories.router.categories_router import categories_router
from app.food_items.router.food_items_router import food_items_router
# from test import test_router

app = FastAPI()
#uvicorn app.main:app --reload

app.include_router(auth_router, tags=["Authentication Routers"])
app.include_router(user_router, tags=["User Routers"])
app.include_router(categories_router, tags=["Categories Routers"])
app.include_router(food_items_router, tags=["Food Items Routers"])
# app.include_router(test_router, tags=['test routers'])
