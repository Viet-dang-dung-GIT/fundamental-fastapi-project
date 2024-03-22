from passlib.context import CryptContext
import re

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def is_valid_email(email):
    regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(regex, email):
        return True
    return False
