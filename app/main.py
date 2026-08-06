from fastapi import FastAPI
from fastapi.responses import HTMLResponse 
from app.authentication.router.authentication_router import auth_router
from app.user.router.user_router import user_router
from app.categories.router.categories_router import categories_router
from app.food_items.router.food_items_router import food_items_router
from app.daily_menu.router.daily_menu_router import daily_menu_router
from app.carts.router.carts_router import carts_router
from app.orders.router.orders_router import orders_router
from app.payments.router.payments_router import payment_router
from app.notifications.router.notification_router import notification_router
# from test import test_router


app = FastAPI(
    title="FoodieFreak",
    version="1.0.0",
    description="""
                Live :
                        Render          :-   https://foodiefreak.onrender.com
                        FastAPI Cloud   :-   https://foodiefreak-d525b704.fastapicloud.dev
                     
                Docs :  https://docs.google.com/document/d/1I_EDXjYwqHvv7pQIcKD75utlpNwWkro4G7vsFGFwGiM
                """,
    contact={
        "name": "Aniket Khomane",
        "url": "https://github.com/k-aniket-01/FoodieFreak/tree/FastAPI",
    }
)
#uvicorn app.main:app --reload

@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <html>
        <head>
            <title>FoodieFreak</title>
        </head>
        <body>
            <h2>FoodieFreak is running</h2>
            <p>
                <a href="/docs">Open Swagger Documentation</a>
            </p>
        </body>
    </html>
    """

    
app.include_router(auth_router, tags=["Authentication Routers"])
app.include_router(user_router, tags=["User Routers"])
app.include_router(categories_router, tags=["Categories Routers"])
app.include_router(food_items_router, tags=["Food Items Routers"])
app.include_router(daily_menu_router, tags=["Daily Menu Routers"])
app.include_router(carts_router, tags=["Cart Routers"])
app.include_router(orders_router, tags=["Order Routers"])
app.include_router(payment_router, tags=["Payment Routers"])
app.include_router(notification_router, tags=["Notification Routers"])
# app.include_router(test_router, tags=['test routers'])
