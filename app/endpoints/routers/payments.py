from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.crud import schemas
from app.crud.database import get_db
from app.service.oauth2 import get_current_user
from app.crud.crud_payments import PaymentMethod
from app.crud import crud_payments as crud

router = APIRouter(
    prefix="/payments",
    tags=['payments']
)


@router.post("/")
async def create_payment(payment_data: schemas.PaymentBase, payments: PaymentMethod, db: Session = Depends(get_db),
                         get_current: Session = Depends(get_current_user)):
    data = crud.create_payment(db, payment_data)
    result = {'payment_data': data, 'payments': payments}
    if payments == PaymentMethod.ONLINE_PAYMENT_GATEWAY:
        return result

    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="un"
    )
    # if payments == PaymentMethod.CREDIT_CARD:
    #     return {'payment': payments}
    #
    # if payments == PaymentMethod.BANK_TRANSFER:
    #     return {'payment': payments}
    #
    # if payments == PaymentMethod.DEBIT_CARD:
    #     return {'payment': payments}
    #
    # if payments == PaymentMethod.CRYPTOCURRENCY:
    #     return {'payment': payments}
    #
    # if payments == PaymentMethod.COD:
    #     return {'payment': payments}
    #
    # if payments == PaymentMethod.E_WALLET:
    #     return {'payment': payments}
    #
    # if payments == PaymentMethod.GIFT_CARD:
    #     return {'payment': payments}
