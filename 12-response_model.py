# To run only this file with uvicorn use: uvicorn 12-response_model:app --reload
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from typing import List, Optional


# Create FastAPI instance
app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: float = 10.5
    tags: List[str] = []

# You can declare the model used for the response with the parameter
# response_model in any of the path operations (get, post, put, delete, etc.).
# The response model is declared in this parameter instead of as a function return
# type annotation, because the path function may not actually return that response
# model but rather return a dict, database object or some other model, and then use
# the response_model to perform the field limiting and serialization.
@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    return item
# FastAPI will use this response_model to:
# - Convert the output data to its type declaration.
# - Validate the data.
# - Add a JSON Schema for the response, in the OpenAPI path operation.
# - Will be used by the automatic documentation systems.
# - Limit the output data to that kind of the model.

items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}

# Your response model could have default values, like description, tax and tags, but you
# might want to omit them from the result if they were not actually stored. Using the
# parameter response_model_exclude_unset=True will exclude those values from the response,
# only the values actually set will be included.
@app.get("/items/{item_id}", response_model=Item, response_model_exclude_unset=True)
async def read_item(item_id: str):
    return items[item_id]

items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The Bar fighters", "price": 62, "tax": 20.2},
    "baz": {
        "name": "Baz",
        "description": "There goes my baz",
        "price": 50.2,
        "tax": 10.5,
    },
}

# You can also use the path operation decorator parameters response_model_include and response_model_exclude.
# They take a set of str with the name of the attributes to include (omitting the rest) or to exclude (including the rest).
# This can be used as a quick shortcut if you have only one Pydantic model and want to remove some data from the output.
# It is still recommended to use the idea of using multiple classes, instead of these parameters.
@app.get(
    "/items/{item_id}/name",
    response_model=Item,
    response_model_include={"name", "description"},  # Just "name" and "description" will be returned from response.
)
async def read_item_name(item_id: str):
    return items[item_id]

@app.get("/items/{item_id}/public", response_model=Item, response_model_exclude={"tax"})  # "Tax" will be excluded from the repsonse.
async def read_item_public_data(item_id: str):
    return items[item_id]


# Input model with the plaintext password
class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Optional[str] = None

# Output model without it
class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None

# Now, whenever a browser is creating a user with a password, the API will return
# the same password in the response.
@app.post("/user_in/", response_model=UserIn)
async def create_user(user: UserIn):
    return user

# Here, even though our path operation function is returning the same input user that
# contains the password, we declared the response_model to be our model UserOut, that
# doesn't include the password
@app.post("/user_out/", response_model=UserOut)
async def create_user(user: UserIn):
    return user
