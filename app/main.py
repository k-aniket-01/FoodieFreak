from fastapi import FastAPI 
from app.routers import authentication, users

app = FastAPI()
#uvicorn app.main:app --reload

app.include_router(authentication.router)
app.include_router(users.router)
