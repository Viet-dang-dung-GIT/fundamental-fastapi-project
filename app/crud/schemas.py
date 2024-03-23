from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        from_attributes = True


class UserDisable(UserBase):
    disabled: bool | None = None


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock_quantity: int


class Product(ProductBase):
    id: int

    class Config:
        # orm_mode = True
        from_attributes = True


class PaymentBase(BaseModel):
    amount: float
    status: str
    payment_method: str


class PaymentCreate(PaymentBase):
    user_id: int


class Payment(PaymentBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    quantity: int
    total_price: float


class OrderCreate(OrderBase):
    user_id: int
    product_id: int
