from fastapi import HTTPException, status
from datetime import date
from app.daily_menu.transformer.daily_menu_transformer import get_daily_menu_transformer
from app.models.common_models import Order, OrderItem, DailyMenu, CartItem
from app.carts.service.carts_service import get_cart_items_service, clear_cart_items_service
from app.daily_menu.service.daily_menu_service import get_daily_menu_today_service, put_daily_menu_service


def post_order_service(db,user):
    user_id = user.id
    cart_id = next((cart.id for cart in user.carts), None)
    if cart_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='CART NOT FOUND')
        
    cart_items = get_cart_items_service(db,user) 
    if len(cart_items['items']) <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='CART IS EMPTY')
    food_ids = [item["food_item_id"] for item in cart_items["items"]]
    daily_menu = (db.query(DailyMenu)
                  .filter(DailyMenu.menu_date == date.today(),
                          DailyMenu.food_item_id.in_(food_ids), 
                          DailyMenu.is_available == True)
                  .all()
                  )
    menu_lookup = {menu.food_item_id: menu for menu in daily_menu}
    for item in cart_items['items']:
        menu_item = menu_lookup.get(item['food_item_id'])
        if menu_item is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"FOOD ITEM {item['name']} NOT AVAILABLE TODAY")
        if item['quantity'] > menu_item.available_qty:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"ONLY {menu_item.available_qty} "
                                       f"QUANTITY OF '{item['name']}' IS AVAILABLE")    
    order = Order(user_id = user_id, 
                  total_amount = cart_items.get("total_amount"), 
                  status = 'Preparing' 
                  )
    try:
        db.add(order)
        db.flush()
        order_items = []
        for item in cart_items["items"]:
            menu_item = menu_lookup[item["food_item_id"]]
            menu_item.available_qty -= item['quantity']
            if menu_item.available_qty == 0:
                menu_item.is_available = False
            order_items.append(OrderItem(order_id = order.id, 
                                        food_item_id = item['food_item_id'],
                                        quantity = item['quantity'],
                                        item_price = item['price'] ))
        db.add_all(order_items) 
        db.query(CartItem).filter(CartItem.cart_id == cart_id).delete(synchronize_session=False)
        db.commit()
        db.refresh(order)
        return order
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f'{e}')