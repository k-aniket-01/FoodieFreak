from app.database import Base
from datetime import datetime, timezone
from sqlalchemy import (
    JSON, Column, String, Integer, ForeignKey, Boolean, Date, DateTime, 
    UniqueConstraint, Enum
)
from sqlalchemy.orm import relationship
from app.utility.enums import OrderStatusEnum, PaymentStatusEnum

class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    description = Column(String(500))

    users = relationship("User",secondary='user_roles', back_populates="roles") #This is not a database column.It tells SQLAlchemy:"A role can have many users.

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(255), unique=True)
    phone = Column(String(20), unique=True)
    password = Column(String(255))
    created_at = Column(DateTime, default=datetime.now)
    is_active = Column(Boolean, default=True)
    # role_id = Column(Integer, ForeignKey("roles.id"))

    roles = relationship("Role", secondary="user_roles", back_populates="users")
    carts = relationship("Cart", back_populates="user")
    orders = relationship("Order", back_populates="user")


class UserRole(Base):
    __tablename__ = 'user_roles'
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    role_id = Column(Integer, ForeignKey("roles.id"), primary_key=True)


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    description = Column(String(500))
    is_active = Column(Boolean, default=True)

    food_items = relationship("FoodItem",back_populates='category')


class FoodItem(Base):
    __tablename__ = 'food_items'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    description = Column(String(500))
    price = Column(Integer)
    is_available = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    is_active = Column(Boolean, default=True)

    category = relationship("Category", back_populates="food_items")
    

class DailyMenu(Base):
    __tablename__ = 'daily_menus'
    __table_args__ = (
                    UniqueConstraint("food_item_id","menu_date"),
    )
    id = Column(Integer, primary_key=True)
    food_item_id = Column(Integer, ForeignKey("food_items.id"))
    menu_date = Column(Date)
    available_qty = Column(Integer)
    is_available = Column(Boolean, default=True)

    food_item = relationship("FoodItem")


class Cart(Base):
    __tablename__ = 'carts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="carts")
    items = relationship("CartItem", back_populates="cart")


class CartItem(Base):
    __tablename__ = 'cart_items'
    __table_args__ = (UniqueConstraint("cart_id","food_item_id"),)
    id = Column(Integer, primary_key=True)
    cart_id = Column(Integer, ForeignKey("carts.id"))
    food_item_id = Column(Integer, ForeignKey("food_items.id"))
    quantity = Column(Integer)
    
    cart = relationship("Cart", back_populates="items")
    food_item = relationship("FoodItem")


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    total_items = Column(Integer)
    total_amount = Column(Integer)
    status = Column(Enum(OrderStatusEnum, name='order_status'),nullable=False,default=OrderStatusEnum.PENDING)
    created_at = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")
    payments = relationship("Payment", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    food_item_id = Column(Integer, ForeignKey("food_items.id"))
    quantity = Column(Integer)
    item_price = Column(Integer)

    order = relationship("Order", back_populates="items")
    food_item = relationship("FoodItem")


class Payment(Base):
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    gateway = Column(String(50))
    gateway_order_id = Column(String(100), index=True)
    gateway_payment_id = Column(String(100), index=True)
    amount = Column(Integer, nullable=False)
    currency = Column(String(10), default='INR')
    payment_method = Column(String(50))
    status = Column(Enum(PaymentStatusEnum, name="payment_status"),
                    default=PaymentStatusEnum.PENDING,
                    nullable=False
                    )
    failure_reason = Column(String(500))
    paid_at = Column(DateTime)
    created_at = Column(DateTime, default=lambda:datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda:datetime.now(timezone.utc), 
                        onupdate=lambda:datetime.now(timezone.utc))

    order = relationship("Order", back_populates="payments")
    events = relationship("PaymentEvent", back_populates="payment")
    refunds = relationship("Refund", back_populates="payment")
    idempotency_keys = relationship("IdempotencyKey", back_populates="payment")
    
    
class PaymentEvent(Base):
    __tablename__ = 'payment_events'
    id = Column(Integer, primary_key=True)
    payment_id = Column(Integer, ForeignKey('payments.id'), nullable=False)
    event_type = Column(String(50), nullable=False)
    status = Column(String(50))
    request_payload = Column(JSON)
    response_payload = Column(JSON)
    created_at = Column(DateTime, default=lambda:datetime.now(timezone.utc))
    
    payment = relationship("Payment", back_populates="events")

class Refund(Base):
    __tablename__ = 'refunds'
    id = Column(Integer, primary_key=True)
    payment_id = Column(Integer, ForeignKey("payments.id"))
    gateway_refund_id = Column(String(100))
    amount = Column(Integer)
    status = Column(String(100))
    speed_requested = Column(String(100))
    speed_processed = Column(String(100))
    created_at = Column(DateTime, default=lambda:datetime.now(timezone.utc))
    updated_at = Column(DateTime, onupdate=lambda:datetime.now(timezone.utc))
    
    payment = relationship("Payment", back_populates="refunds")
    
class IdempotencyKey(Base):
    __tablename__ = 'idempotency_keys'
    id = Column(Integer, primary_key=True)
    key = Column(String(255), unique=True, nullable=False)
    payment_id = Column(Integer, ForeignKey("payments.id"))
    endpoint = Column(String(200))
    created_at = Column(DateTime, default=lambda:datetime.now(timezone.utc)) 
    
    payment = relationship("Payment", back_populates="idempotency_keys")
    
    
class Notification(Base):
    __tablename__ = 'notifications'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(255))
    message = Column(String(1000))
    is_read = Column(Boolean, default=False)

    user = relationship("User")


class AuditLog(Base):
    __tablename__ = 'audit_logs'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String(255))

    user = relationship("User")