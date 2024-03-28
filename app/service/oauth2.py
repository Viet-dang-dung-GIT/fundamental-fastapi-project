import token

from jose import JWTError, jwt
from sqlalchemy.orm import Session as db

from app.crud import crud_users
from app.crud.schemas import TokenData
from ..service import token as aut

from starlette import status
from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def get_current_user(data: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(data, aut.SECRET_KEY, algorithms=[aut.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = crud_users.get_user_by_email(db, user_email=token_data.email)
    if user is None:
        raise credentials_exception
    return user
