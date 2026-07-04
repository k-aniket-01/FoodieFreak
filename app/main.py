from fastapi import FastAPI 
from app.authentication.router.authentication_router import auth_router
from app.user.router.user_router import user_router
# from test import test_router

app = FastAPI()
#uvicorn app.main:app --reload

app.include_router(auth_router, tags=["Authentication Routers"])
app.include_router(user_router,tags=['User Routers'])
# app.include_router(test_router, tags=['test routers'])
