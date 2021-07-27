# To run only this file with uvicorn use: uvicorn 16-body_updates:app --reload
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import List, Optional


# Create FastAPI instance
app = FastAPI()


class Item(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    tax: float = 10.5
    tags: List[str] = []

items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}

@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str):
    return items[item_id]

# To update an item you can use the HTTP PUT operation.
# You can use the jsonable_encoder to convert the input data to data that can be stored as JSON.
# For example, converting datetime to str.
@app.put("/items/put/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    update_item_encoded = jsonable_encoder(item)
    items[item_id] = update_item_encoded
    return update_item_encoded

# If you want to receive partial updates, it's very useful to use the parameter exclude_unset in Pydantic's
# model's .dict(). That would generate a dict with only the data that was set when creating the item model,
# excluding default values. Then you can use this to generate a dict with only the data that was set (sent in
# the request), omitting default values.
@app.patch("/items/patch/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    stored_item_data = items[item_id]
    stored_item_model = Item(**stored_item_data)
    update_data = item.dict(exclude_unset=True)
    updated_item = stored_item_model.copy(update=update_data)
    items[item_id] = jsonable_encoder(updated_item)
    return updated_item


'''
In summary, to apply partial updates you would:
- (Optionally) use PATCH instead of PUT.
- Retrieve the stored data.
- Put that data in a Pydantic model.
- Generate a dict without default values from the input model (using exclude_unset). This way you can update only
the values actually set by the user, instead of overriding values already stored with default values in your model.
- Create a copy of the stored model, updating it's attributes with the received partial updates (using the update parameter).
- Convert the copied model to something that can be stored in your DB (for example, using the jsonable_encoder). This is
comparable to using the model's .dict() method again, but it makes sure (and converts) the values to data types that can be
converted to JSON, for example, datetime to str.
- Save the data to your DB.
- Return the updated model.
'''

