from fastapi import FastAPI 
from app.routers import authentication, users
from test import test_router

app = FastAPI()
#uvicorn app.main:app --reload

app.include_router(authentication.router, tags=["Authentication"])
app.include_router(users.router,tags=['Users Router'])
app.include_router(test_router, tags=['test routers'])
