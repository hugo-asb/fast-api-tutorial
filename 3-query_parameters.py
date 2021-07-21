# To run only this file with uvicorn use: uvicorn 3-query_parameters:app --reload
from fastapi import FastAPI
from typing import Optional


# Create FastAPI instance
app = FastAPI()


# When you declare other function parameters that are not part of the path parameters,
# they are automatically interpreted as "query" parameters.
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

# The query is the set of key-value pairs that go after the ? in a URL, separated by & characters.
# The query parameters are: skip and limit (default values are 0 and 10). Path = /items/?skip=0&limit=10 for example.
@app.get("/items/")
async def read_items(skip: int=0, limit: int=10):
    return fake_items_db[skip: skip + limit]

# For optionals query parameters, set the default value (None to don't add an especific value).
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Optional[str] = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:  # The boolean value will be parsed with values 0/1, true/false, on/off, regardeless uppercase/lowercase.
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

# If a default value is not set to a query parameter, it will be required to be passed.
# In this case: needy - required string, skip - int with default value 1, limit - optional int.
@app.get("/items_obr/{item_id}")
async def read_user_item(
    item_id: str,
    needy: str,
    skip: int = 0,
    limit: Optional[int] = None
):
    item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
    return item


# You can declare multiple path parameters and query parameters at the same time, FastAPI knows which is which.
# And you don't have to declare them in any specific order, They will be detected by name
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int,
    item_id: str,
    q: Optional[str] = None,
    short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item
