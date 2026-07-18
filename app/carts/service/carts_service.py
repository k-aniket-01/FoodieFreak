from fastapi import HTTPException,status
from sqlalchemy import func
from app.models.common_models import CartItem, Cart, FoodItem
from app.carts.transformer.carts_transformer import get_cart_items_transformer,get_cart_summery_transformer
from app.carts.schema.carts_schema import SummerySchema
def post_cart_item_service(body, db ,user):
    body = body.model_dump()
    quantity = body.get('quantity')
    if quantity is None or quantity<=0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=['QUANTITY MUST BE GREATER THAN 0'])
    cart_id = next((cart.id for cart in user.carts), None)
    if cart_id is None:
        cart = Cart(user_id = user.id)
        db.add(cart)
        db.flush()
        cart_id = cart.id
    product = db.query(CartItem).filter(CartItem.food_item_id == body['food_item_id'],
                                        CartItem.cart_id == cart_id).first()
    if product:
        product.quantity += quantity
    else:
        body['cart_id'] = cart_id
        data = CartItem(**body)
        db.add(data)
    try:
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"{e}")
    
    
def get_cart_items_service(db, user):
    cart_id = next((cart.id for cart in user.carts), None)
    if cart_id is None:
        return []
    summery = (db.query(CartItem.cart_id,
                        func.count(CartItem.id).label('total_items'),
                        func.sum(FoodItem.price * CartItem.quantity).label('total_amount')
                        )
            .join(FoodItem, CartItem.food_item_id == FoodItem.id)
            .group_by(CartItem.cart_id)
            .filter(CartItem.cart_id == cart_id)
            .first()
            )
    if summery is None :
        return {"cart_id":cart_id,
                "message":"CART IS EMPTY",
                "total_items": 0,
                "total_amount":0}
    items = (db.query(CartItem.id,
                      CartItem.food_item_id,
                      FoodItem.name,
                      FoodItem.price,
                      CartItem.quantity,
                      (FoodItem.price * CartItem. quantity).label('sub_total')
                      )
             .join(FoodItem, CartItem.food_item_id == FoodItem.id)
             .filter(CartItem.cart_id == cart_id)
             .all()
             )
    response_data = get_cart_items_transformer(summery, items)
    return response_data


def put_cart_item_service(id,body,db,user):
    cart_id = next((cart.id for cart in user.carts), None)
    if body.quantity <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail=['QUANTITY MUST BE GREATER THAN 0'])
    if cart_id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=['CART NOT FOUND'])
    item = (db.query(CartItem)
            .filter(CartItem.cart_id == cart_id,
                    CartItem.id == id)
            .first()
            )
    if item:
        for k,v in body.model_dump().items():
            setattr(item, k, v)
        db.commit()
        return True
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail=['ITEM NOT FOUND'])
    
    
def delete_cart_item_service(id,db,user):
    cart_id = next((cart.id for cart in user.carts), None)
    if cart_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=['CART NOT FOUND'])
    item = (db.query(CartItem)
            .filter(CartItem.cart_id == cart_id,
                    CartItem.id == id)
            .first()
            )
    if item:
        db.delete(item)
        db.commit()
        return True
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=['ITEM NOT FOUND'])
    

def clear_cart_items_service(db,user):
    cart_id = next((cart.id for cart in user.carts), None)
    if cart_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=['CART NOT FOUND'])
    items = (db.query(CartItem)
             .filter(CartItem.cart_id == cart_id)
             .all()
             )
    if items is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=['NO ITEM FOUND TO REMOVE'])
    try:
        db.delete(*items)
        db.commit()
        return True
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"{e}")
        

def get_cart_summery_service(db, user):
    cart_id = next((cart.id for cart in user.carts), None)
    if cart_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='CART NOT FOUND')
    data = (db.query(CartItem.cart_id,
                     func.count(CartItem.id).label('total_items'),
                     func.sum(CartItem.quantity * FoodItem.price).label('total_amount')
                     )
                     .join(FoodItem, CartItem.food_item_id == FoodItem.id)
                     .group_by(CartItem.cart_id)
                     .filter(CartItem.cart_id == cart_id)
                     .first()
                     )
    print(data)
    if data is None :
        return {"cart_id":cart_id,
                "message":"CART IS EMPTY",
                "total_items": 0,
                "total_amount":0}
    response_data = get_cart_summery_transformer(data)
    return response_data