from fastapi import HTTPException,status
from app.models.common_models import CartItem, Cart


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
    