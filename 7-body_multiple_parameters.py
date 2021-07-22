# To run only this file with uvicorn use: uvicorn 7-body_multiple_parameters:app --reload
from fastapi import FastAPI, Path, Body
from pydantic import BaseModel
from typing import Optional


# Create FastAPI instance
app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


class User(BaseModel):
    username: str
    full_name: Optional[str] = None


# you can mix Path, Query and request body parameter declarations freely and FastAPI
# will know what to do. And you can also declare body parameters as optional, by setting
# the default to None
@app.put("/items/single_body/{item_id}")
async def update_item(
    *,
    item_id: int = Path(..., title="The ID of the item to get", ge=0, le=1000),
    q: Optional[str] = None,
    item: Optional[Item] = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results

# You can also declare multiple body parameters, e.g. item and user. FastAPI will
# notice that there are more than one body parameters in the function (two parameters
# that are Pydantic models).
@app.put("/items/many_body/{item_id}")
async def update_item(item_id: int, item: Item, user: User):
    results = {"item_id": item_id, "item": item, "user": user}
    return results

# The same way there is a Query and Path to define extra data for query and path parameters,
# FastAPI provides an equivalent Body.
@app.put("/items/singular_v/{item_id}")
async def update_item(
    item_id: int, item: Item, user: User, importance: int = Body(...)
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    return results

# By default, singular values are interpreted as query parameters (no need to explicitly add a Query).
# So, can also declare additional query parameters whenever you need, additional to any body parameters.
# Body also has all the same extra validation and metadata parameters as Query,Path, etc.
@app.put("/items/query/{item_id}")
async def update_item(
    *,
    item_id: int,
    item: Item,
    user: User,
    importance: int = Body(..., gt=0),
    q: Optional[str] = None
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    if q:
        results.update({"q": q})
    return results

# Let's say you only have a single item body parameter from a Pydantic model Item.
# By default, FastAPI will then expect its body directly. But if you want it to expect a JSON with a
# key item and inside of it the model contents, as it does when you declare extra body parameters, you
# can use the special Body parameter embed.
@app.put("/items/embeded/{item_id}")
async def update_item(item_id: int, item: Item = Body(..., embed=True)):
    results = {"item_id": item_id, "item": item}
    return results
