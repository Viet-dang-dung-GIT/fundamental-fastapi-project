from fastapi import Depends, FastAPI, BackgroundTasks

from .dependencies import get_query_token, get_token_header, write_notification
from .internal import admin
from .routers import items, users

app = FastAPI(dependencies=[Depends(get_query_token)])

# include router from the submodules users and items
# with include_router we can add each APIRouter
app.include_router(users.router)
app.include_router(items.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}


@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}
