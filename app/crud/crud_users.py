from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.crud import models
from app.crud.schemas import UserCreate
from app.service.security import hash_password
from app.dependencies import validate_email


async def user_exists(db: Session, username: str, email: str):
    user_by_username = db.query(models.User).filter(models.User.username == username).first()
    if user_by_username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

    user_by_email = db.query(models.User).filter(models.User.email == email).first()
    if user_by_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")


async def create_user(db: Session, user: UserCreate):
    validate_email(user.email)
    await user_exists(db, user.username, user.email)
    db_user = models.User(
        db, username=user.username, email=user.email, password=hash_password(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


async def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


async def get_users(db: Session, skip: int = 0, limit: int = 15):
    return db.query(models.User).offset(skip).limit(limit).all()


async def get_user_by_email(db: Session, user_email: str):
    return db.query(models.User).filter(models.User.email == user_email).first()


async def get_user_by_name(db: Session, user_name: str):
    return db.query(models.User).filter(models.User.name == user_name).first()


async def update_user(db: Session, user_id: int, user_data: UserCreate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        for key, value in user_data.dict().items():
            setattr(db_user, key, value)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    return None


async def update_user_by_email(db: Session, user_email: str):
    db_user_email = db.query(models.User).filter(models.User.email == user_email).first()
    if db_user_email:
        for key, value in db_user_email.dict().items():
            if key in ["email"]:
                setattr(db_user_email, key, value)
        db.add(db_user_email)
        db.commit()
        db.refresh(db_user_email)
        return db_user_email
    return None


async def update_user_by_password():
    pass


async def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False
