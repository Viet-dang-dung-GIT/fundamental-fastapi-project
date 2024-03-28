from starlette import status
from datetime import timedelta
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException

from ..crud import database, models
from ..crud.database import SessionLocal
from ..service import security, token
from ..crud.schemas import Register
from ..crud.crud_users import get_user_by_name, check_username_exists
from .security import hash_password, verify_password, validate_email
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    tags=["Authentication"]
)

session = SessionLocal
db = session()


@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), data: Session = Depends(database.get_db)):
    user = data.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"{request.username} Invalid")
    if not security.verify_password(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect password")

    access_token_expires = timedelta(minutes=token.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = token.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register/")
async def register_user(user: Register):
    validate_email(user.email)
    if not (user.password == user.repassword):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="incorrect password"
        )
    hashed_password = hash_password(user.password)
    db_user = models.User(username=user.username, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


async def authenticate_user(db: Session, username: str, password: str):
    user = await get_user_by_name(db, username)
    if not user or not verify_password(password, user["password"]):
        return False
    return user
