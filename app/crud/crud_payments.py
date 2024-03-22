from sqlalchemy.orm import Session

from app.crud import models
from app.crud.schemas import PaymentBase


def create_payment(db: Session, payment: PaymentBase):
    db_payment = models.Payment(**payment.dict())
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment


def get_payment(db: Session, payment_id: int):
    return db.query(models.Payment).filter(models.Payment.id == payment_id).first()


def update_payment(db: Session, payment_id: int, payment_data: PaymentBase):
    db_payment = db.query(models.Payment).filter(models.Payment.id == payment_id).first()
    if db_payment:
        for key, value in payment_data.dict().items():
            setattr(db_payment, key, value)
        db.add(db_payment)
        db.commit()
        db.refresh(db_payment)
        return db_payment
    return None


def delete_payment(db: Session, payment_id: int):
    db_payment = db.query(models.Payment).filter(models.Payment.id == payment_id).first()
    if db_payment:
        db.delete(db_payment)
        db.commit()
        return True
    return False
