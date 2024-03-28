from starlette import status
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.crud import models
from app.crud.schemas import UserCreate
from app.dependencies import validate_email
from app.service.security import hash_password


def check_username_exists(db: Session, username: str) -> bool:
    existing_user = db.query(models.User).filter(models.User.username == username).first()
    return existing_user is not None


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
    db_user = models.User(username=user.username, email=user.email, password=hash_password(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


async def get_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User id: {user_id} not found"
        )
    return user


async def get_all_users(db: Session):
    user = db.query(models.User).all()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No any user create")
    return user


async def get_users(db: Session, skip: int = 0, limit: int = 15):
    return db.query(models.User).offset(skip).limit(limit).all()


async def get_user_by_email(db: Session, email: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User email {email} not found"
        )
    return user


async def get_user_by_name(db: Session, user_name: str):
    user = db.query(models.User).filter(models.User.name == user_name).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User name {user_name} not found"
        )
    return user


async def update_user(db: Session, user_id: int, user_data: UserCreate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()

    if db_user:
        if "email" in user_data.dict():
            user_data.email = validate_email(user_data.email)
        if "password" in user_data.dict():
            user_data.password = hash_password(user_data.password)
        for key, value in user_data.dict().items():
            setattr(db_user, key, value)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User id{user_id}:{user_data} not available"
    )


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
        return 'delete successfully'
    return False
