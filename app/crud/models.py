from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from app.crud.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

    products = relationship("Product", back_populates="owner")
    payments = relationship("Payment", back_populates="user")
    orders = relationship("Order", back_populates="user")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, nullable=False)

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="products")

    orders = relationship("Order", back_populates="product")


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    amount = Column(Float)
    status = Column(String)
    payment_method = Column(String)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="payments")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    quantity = Column(Integer)
    total_price = Column(Float)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="orders")

    product_id = Column(Integer, ForeignKey("products.id"))
    product = relationship("Product", back_populates="orders")

    @property
    def calculate_total_price(self):
        return self.quantity * self.product.price
