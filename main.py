from enum import Enum

from fastapi import FastAPI
from pydantic import BaseModel


class Item(Enum):
    image = "image"
    files = "files"


# it's request body
class Items(BaseModel):
    image: str | None = None
    files: str | None = None


class ModelE(BaseModel):
    name: str
    description: str | None = None
    tax: int | None = None
    item: list[Items | None]


app = FastAPI()


# 1 part parameters
@app.get("/items/")
async def get_items():
    return {"item": "id", "message": "this is path parameter"}


# 2 query parameters
fake_user_db = [{'item_id': 10, "message": "it's ten"}, {"item_id": 20, "message": "it's twenty"}]


# here path like 127.0.0.1/items/numbers/skip?=0&limit=10
@app.get("/items/numbers")
async def get_number(skip: int = 0, limit: int = 10):
    result = fake_user_db[skip: skip + limit]
    return result


@app.get("/{item_id}/")
async def read_items(item_id: int, q: str | None = None, short: bool = False):
    result = {"item": item_id}
    if q:
        result.update({"q": q})
    if not short:
        result.update(
            {"description": "Maybe not true"}
        )
    return result


@app.get("/items/{item_id}/")
async def get_items_id(item_id: int, message: str | None = None):
    result = list['item_id': item_id, 'message': message]
    return result


# 3 Request Body

# in request body editor have hint and use model with name model + "." + field
# e.g. item.image

@app.post("/items/request/")
async def request_body(item: Items):
    return item


# request + path + query parameter like
@app.put("items/{item_id}/")
async def request_path_query(item_id: str, item: Items, q: str | None = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result
# 4 Query Parameters and string validation
# 5 Path Parameters and Numeric Validations
# 6 Body multiple Parameters
# 7 Body - fields
# 8 Body- Nested Models
