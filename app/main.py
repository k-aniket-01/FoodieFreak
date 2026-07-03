from fastapi import FastAPI 
from app.authentication.router.authentication_router import auth_router
# from app.routers.users import router
# from test import test_router

app = FastAPI()
#uvicorn app.main:app --reload

app.include_router(auth_router, tags=["Authentication"])
# app.include_router(router,tags=['Users Router'])
# app.include_router(test_router, tags=['test routers'])
