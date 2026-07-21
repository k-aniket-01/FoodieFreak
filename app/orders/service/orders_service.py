from fastapi import HTTPException, status
from datetime import date
from sqlalchemy import func
from app.models.common_models import Order, OrderItem, DailyMenu, CartItem, FoodItem
from app.utility.response_utility import apply_pagination, apply_filters,PaginationRequestSchema
from app.carts.service.carts_service import get_cart_items_service
from app.orders.transformer.orders_transformer import  (
    get_id_order_transformer, get_orders_history_transformer, get_order_status_transformer
)

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
                  .with_for_update() #for the prevention 2 users place orders simultaneously
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
                  total_items = len(cart_items["items"]),
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
        (db.query(CartItem)
           .filter(CartItem.cart_id == cart_id)
           .delete(synchronize_session=False)) #for multiple items delete in one query
        db.commit()
        db.refresh(order)
        return order
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')
    
    
def get_id_order_service(id,db,user):
    user_id = user.id
    summery = (db.query(OrderItem.order_id,
                        Order.user_id,
                        Order.status,
                        func.count(OrderItem.order_id).label('total_items'),
                        func.sum(OrderItem.quantity * OrderItem.item_price).label('total_amount')
                        )
               .join(OrderItem, Order.id == OrderItem.order_id)
               .group_by(OrderItem.order_id, Order.user_id, Order.status)
               .filter(Order.id == id, Order.user_id == user_id)
               .first()
               )
    if summery is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= {"order_id":id,
                                     "message":"NO ORDER FOUND",
                                     "total_items": 0,
                                     "total_amount":0,
                                     "items": []})
    items = (db.query(Order.id, 
                      OrderItem.food_item_id,
                      FoodItem.name.label('food_name'),
                      OrderItem.quantity,
                      OrderItem.item_price,
                      (OrderItem.quantity * OrderItem.item_price).label('sub_total')
                      )
             .join(OrderItem, Order.id == OrderItem.order_id)
             .join(FoodItem, OrderItem.food_item_id == FoodItem.id)
             .filter(OrderItem.order_id == id, Order.user_id == user_id)
             .all()
             )
    if items is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= {"order_id":id,
                                     "message":"NO ORDER FOUND",
                                     "total_items": 0,
                                     "total_amount":0,
                                     "items": []})
    response_data = get_id_order_transformer(summery, items)
    return response_data
 

def get_orders_history_service(body, db, user):
    query = (db.query(Order.id,
                      Order.user_id,
                      Order.status,
                      Order.total_items,
                      Order.total_amount,
                      Order.created_at
                      )
              .filter(Order.user_id == user.id)
              )
    query = apply_filters(body=body,model=Order,query=query)
    pagination = body.pagination
    if pagination is None:
        pagination = PaginationRequestSchema()
    if body.pagination:
       query, pagination = apply_pagination(body=body.pagination,query=query)
    query = query.all()
    response_data = get_orders_history_transformer(query, pagination)
    return response_data


def cancel_order_service(id, db, user):
    query = (db.query(Order)
             .filter(Order.id == id,
                     Order.user_id == user.id)
             .first()
             )
    if query is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="ORDER DETAILS NOT FOUND")
    if query.status in ['COMPLETED','READY','PREPARING']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"'{query.status}' ORDER CAN NOT BE CANCELLED")
    if query.status == 'CANCELED':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="ORDER IS ALREADY CANCELED")
    try:    
        query.status = 'CANCELED'
        db.commit()
        db.refresh(query)
        return query
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"{e}")
        

def get_order_status_service(id, db, user):
    order = (db.query(Order)
             .filter(Order.id == id,
                     Order.user_id == user.id)
             .first()
             )
    if order is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='ORDER NOT FOUND')
    response_data = get_order_status_transformer(order)
    return response_data