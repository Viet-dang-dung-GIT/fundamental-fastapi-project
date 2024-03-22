import re
from typing import Annotated

from fastapi import Header, HTTPException, BackgroundTasks, Depends


async def get_token_header(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def get_query_token(token: str):
    if token != "jessica":
        raise HTTPException(status_code=400, detail="No Jessica token provided")


# define background task to be run after returning a response
def write_notification(email: str, message=""):
    with open("../log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)


def write_log(message: str):
    with open('../log.txt', mode='a') as log:
        log.write(message)


def get_query(background_tasks: BackgroundTasks, q: str | None = None):
    if q:
        message = f"found query: {q}\n"
        background_tasks.add_task(write_log, message)


def is_valid_email(email):
    regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(regex, email) is not None


def validate_email(email: str = Depends()):
    if not is_valid_email(email):
        raise ValueError("Invalid email format")
    return email


