from fastapi import FastAPI 
from app.routers import authentication

app = FastAPI()
#uvicorn app.main:app --reload

app.include_router(authentication.router)