from sqlalchemy.orm import Session

from app.crud import models
from app.crud.schemas import OrderCreate


def create_order(db: Session, order: OrderCreate):
    db_order = models.Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()


def get_orders_by_user(db: Session, user_id: int):
    return db.query(models.Order).filter(models.Order.user_id == user_id).all()

def update_order(db: Session, order_id: int, order_data: OrderCreate):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order:
        for key, value in order_data.dict().items():
            setattr(db_order, key, value)
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        return db_order
    return None


def delete_order(db: Session, order_id: int):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order:
        db.delete(db_order)
        db.commit()
        return True
    return False
