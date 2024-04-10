from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import Response

from app.crud import crud_users as crud, schemas
from app.crud.database import get_db
from app.service.oauth2 import get_current_user

# instance
router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get("/", response_model=list[schemas.UserBase])
async def read_users(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    list_user = await crud.get_all_users(db)
    return list_user


@router.get("/id/{user_id}")
async def read_user_by_id(user_id: int, db: Session = Depends(get_db),
                          current_user: schemas.User = Depends(get_current_user)):
    return await crud.get_user(db, user_id)


@router.get("/name/{user_name}")
async def read_user(user_name: str, db: Session = Depends(get_db),
                    current_user: schemas.User = Depends(get_current_user)):
    return await crud.get_user_by_name(db, user_name)


@router.get("/email/{user_email}")
async def read_user_by_email(user_email: str, db: Session = Depends(get_db),
                             current_user: schemas.User = Depends(get_current_user)):
    return await crud.get_user_by_email(db, user_email)


@router.post("/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db),
                      current_user: schemas.User = Depends(get_current_user)):
    return await crud.create_user(db, user)


@router.put("/", response_model=schemas.UserCreate)
async def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db),
                      current_user: schemas.User = Depends(get_current_user)):
    return await crud.update_user(db, user_id, user)
