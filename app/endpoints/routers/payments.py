from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud.crud_payments import PaymentMethod
from app.crud.database import get_db
from app.service.oauth2 import get_current_user

router = APIRouter(
    prefix="payments",
    tags=['payments']
)


@router.post("/")
async def create_payment(payments: PaymentMethod, db: Session = Depends(get_db), get_current : Session = Depends(get_current_user)):
    if payments.value == PaymentMethod.ONLINE_PAYMENT_GATEWAY:
        return {'payment': payments}

