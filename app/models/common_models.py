from datetime import datetime
from app.database import Base
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, Date, DateTime
from sqlalchemy.orm import relationship

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
    phone = Column(String(20))
    password_hash = Column(String(255))
    created_at = Column(DateTime, default=datetime.now)
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
    name = Column(String(100))
    description = Column(String(500))

    food_items = relationship("FoodItem",back_populates='category')


class FoodItem(Base):
    __tablename__ = 'food_items'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(String(500))
    price = Column(Integer)
    category_id = Column(Integer, ForeignKey("categories.id"))

    category = relationship("Category", back_populates="food_items")
    

class DailyMenu(Base):
    __tablename__ = 'daily_menus'
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
    total_amount = Column(Integer)
    status = Column(String(50))

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")
    payment = relationship("Payment", back_populates="order", uselist=False)

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
    amount = Column(Integer)
    transaction_id = Column(String(100))
    payment_method = Column(String(100))
    status = Column(String(100))

    order = relationship("Order", back_populates='payment')


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