from fastapi import FastAPI

app = FastAPI()
#uvicorn main:app --reload

@app.get('/')
def greet():
    return {"message":"Hello FoodieFreak Dev"}