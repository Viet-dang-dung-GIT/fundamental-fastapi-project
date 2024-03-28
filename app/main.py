import time

# from .dependencies import get_query_token, get_token_header
from app.endpoints.routers import users, products
from .service import auth
from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles

# app = FastAPI(dependencies=[Depends(get_query_token)])
app = FastAPI()
# app.mount("/static", StaticFiles(directory="static"), name="static")


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(products.router)


# app.include_router(
#     admin.router,
#     prefix="/admin",
#     tags=["admin"],
#     dependencies=[Depends(get_token_header)],
#     responses={418: {"description": "I'm a teapot"}},
# )


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
