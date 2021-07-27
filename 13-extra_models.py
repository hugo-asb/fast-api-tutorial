# To run only this file with uvicorn use: uvicorn 13-extra_models:app --reload
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from typing import Optional, Union, List, Dict


# Create FastAPI instance
app = FastAPI()


# It is common to have more than one related model, especially when:
# - The input model needs to be able to have a password.
# - The output model should not have a password.
# - The database model would probably need to have a hashed password.
class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Optional[str] = None

class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None

class UserInDB(BaseModel):
    username: str
    hashed_password: str
    email: EmailStr
    full_name: Optional[str] = None

def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password

# user_in is a Pydantic model of class UserIn.
# Pydantic models have a .dict() method that returns a dict with the model's data.
# If we take a dict like user_dict and pass it to a function (or class) with
# **user_dict, Python will "unwrap" it. It will pass the keys and values of the user_dict
# directly as key-value arguments.
def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print(user_in.dict())  # This will print the model's data dict.
    print(user_in_db)  # This will print the dict above as key-value arguments.
    print("User saved! ..not really")
    return user_in_db

@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved


'''
Reducing code duplication is one of the core ideas in FastAPI.
We can declare a UserBase model that serves as a base for our other models. And then we can
make subclasses of that model that inherit its attributes (type declarations, validation, etc).
All the data conversion, validation, documentation, etc. will still work as normally.

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None

class UserIn(UserBase):
    password: str

class UserOut(UserBase):
    pass

class UserInDB(UserBase):
    hashed_password: str
'''


# You can declare a response to be the Union of two types, that means, that the response would be
# any of the two. It will be defined in OpenAPI with anyOf.
class BaseItem(BaseModel):
    description: str
    type: str

class CarItem(BaseItem):
    type = "car"

class PlaneItem(BaseItem):
    type = "plane"
    size: int

items = {
    "item1": {"description": "All my friends drive a low rider", "type": "car"},
    "item2": {
        "description": "Music is my aeroplane, it's my aeroplane",
        "type": "plane",
        "size": 5,
    },
}

@app.get("/items/{item_id}", response_model=Union[PlaneItem, CarItem])
async def read_item(item_id: str):
    return items[item_id]

# The same way, you can declare responses of lists of objects.
class Item(BaseModel):
    name: str
    description: str

items = [
    {"name": "Foo", "description": "There comes my hero"},
    {"name": "Red", "description": "It's my aeroplane"},
]

@app.get("/items/", response_model=List[Item])
async def read_items():
    return items


# You can also declare a response using a plain arbitrary dict, declaring just the type of the keys
# and values, without using a Pydantic model. This is useful if you don't know the valid field/attribute
# names (that would be needed for a Pydantic model) beforehand.
@app.get("/keyword-weights/", response_model=Dict[str, float])
async def read_keyword_weights():
    return {"foo": 2.3, "bar": 3.4}
