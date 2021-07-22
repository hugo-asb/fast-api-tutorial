# To run only this file with uvicorn use: uvicorn 9-body_nested_models:app --reload
from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl
from typing import Optional, List, Set, Dict


# Create FastAPI instance
app = FastAPI()


# You can define, validate, document, and use arbitrarily deeply nested models (thanks to Pydantic).
# You can define an attribute to be a subtype (a Python list in this case).
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: list = []

# tags be a list of something, although it doesn't declare the type of each of them.
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results


# To declare types that have type parameters (internal types), like list, dict, tuple:
# - Import them from the typing module
# - Pass the internal type(s) as "type parameters" using square brackets: [ and ]
class ItemList(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: List[str] = []

# Here, tags will be a list of strings.
@app.put("/items/list/{item_id}")
async def update_item(item_id: int, item: ItemList):
    results = {"item_id": item_id, "item": item}
    return results


# Python has a special data type for sets of unique items, the set. Then we can import Set
# and declare tags as a set of str.
class ItemSet(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: Set[str] = set()

# With this, even if you receive a request with duplicate data, it will be converted to a set
# of unique items.
@app.put("/items/set/{item_id}")
async def update_item(item_id: int, item: ItemSet):
    results = {"item_id": item_id, "item": item}
    return results


# Each attribute of a Pydantic model has a type, but that type can itself be another Pydantic model.
# So, you can declare deeply nested JSON "objects" with specific attribute names, types and validations,
# all that, arbitrarily nested.
class Image(BaseModel):  # This is the submodel
    url: HttpUrl  # This is a type from pydantic and will be checked to be a valid URL.
    name: str

class ItemNested(BaseModel):
    name: str
    price: float
    description: Optional[str] = None
    tax: Optional[float] = None
    tags: Set[str] = []
    image: Optional[Image] = None  # Here the submodel is used as a type of an attribute.

@app.put("/items/nested/{item_id}")
async def update_item(item_id: int, item: ItemNested):
    results = {"item_id": item_id, "item": item}
    return results

'''
You can also use Pydantic models as subtypes of list, set, etc:
    'images: Optional[List[Image]] = None'
This will expect (convert, validate, document, etc) a JSON body like:
{
    ...,
    "images": [
        {
            "url": "http://example.com/baz.jpg",
            "name": "The Foo live"
        },
        {
            "url": "http://example.com/dave.jpg",
            "name": "The Baz"
        }
    ]
}
'''


# You can define arbitrarily deeply nested models:
class ItemDeeply(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: Set[str] = set()
    images: Optional[List[Image]] = None

# Offer has a list of Items, which in turn have an optional list of Images.
class Offer(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    items: List[ItemDeeply]

@app.post("/offers/")
async def create_offer(offer: Offer):
    return offer


# You can also declare a body as a dict with keys of some type and values of other type.
# Without having to know beforehand what are the valid field/attribute names.
# This would be useful if you want to receive keys that you don't already know.
# In this case, it would accept any dict as long as it has int keys with float values
# ({ "12": 10.5}, as a body request, for example).
@app.post("/index-weights/")
async def create_index_weights(weights: Dict[int, float]):
    return weights
# Even though the API clients can only send strings as keys, as long as those strings
# contain pure integers, Pydantic will convert them and validate them. And the dict received
# as weights will actually have int keys and float values.
