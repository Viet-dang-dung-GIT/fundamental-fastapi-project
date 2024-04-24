from typing import List
from starlette import status
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, requests

from ...crud import schemas
from app.crud.database import get_db
from ...service.oauth2 import get_current_user
from app.crud.crud_products import get_product
from app.crud.crud_orders import get_order, get_orders_by_user, create_order


router = APIRouter(
    prefix="orders",
    tags=["orders"]
)


@router.post("/place-order/", response_model=schemas.Order)
def place_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    product = get_product(db, order.product_id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    if product.stock_quantity < order.quantity:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient stock quantity")
    # Update stock quantity
    product.stock_quantity -= order.quantity
    db.commit()
    # Create new order
    return create_order(db, order)


@router.get("/order-history/", response_model=List[schemas.Order])
def order_history(user_id: int, db: Session = Depends(get_db),
                  current_user: Session = Depends(get_current_user)):
    orders = get_orders_by_user(db, user_id)
    return orders


@router.post("/simulate-payment/")
def simulate_payment(order_id: int, db: Session = Depends(get_db),
                     current_user: Session = Depends(get_current_user)):
    order = get_order(db, order_id)
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    # Update payment status
    order.payment_status = "Paid"
    db.commit()
    return {"message": "Payment processed successfully"}
