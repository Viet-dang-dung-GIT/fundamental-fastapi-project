from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud.database import SessionLocal
from app.crud import crud_users as crud, schemas
from sql_app.main import get_db

# instance
router = APIRouter()


@router.get("/users/", tags=["users"])
async def read_users(db: Session = Depends(SessionLocal)):
    list_users = crud.get_users(db)
    return list_users


@router.get("/users/{user_id}", tags=["users"])
async def read_user_by_id(user_id: int, db: Session = Depends(SessionLocal)):
    return crud.get_user(db, user_id)


@router.get("/users/{user_name}", tags=["users"])
async def read_user(user_name: str, db: Session = Depends(SessionLocal)):
    only_user = crud.get_user_by_name(db, user_name)
    return only_user


@router.get("/users/{user_email}")
async def read_user_by_email(user_email: str, db: Session = Depends(SessionLocal)):
    return crud.get_user_by_email(db, user_email)


@router.post("/users/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)
