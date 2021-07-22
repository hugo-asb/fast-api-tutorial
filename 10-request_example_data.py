# To run only this file with uvicorn use: uvicorn 10-request_example_data:app --reload
from fastapi import FastAPI, Body
from typing import Optional
from pydantic import BaseModel, Field


# Create FastAPI instance
app = FastAPI()


'''
You can declare examples of the data your app can receive.
Here are several ways to do it.
'''

# Pydantic schema_extra.
# You can declare an example for a Pydantic model using Config and schema_extra.
class ItemSchemaExtra(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Foo",
                "description": "A very nice Item",
                "price": 35.4,
                "tax": 3.2,
            }
        }
# That extra info will be added as-is to the output JSON Schema for that model, and it
# will be used in the API docs.

@app.put("/items/schema_extra/{item_id}")
async def update_item(item_id: int, item: ItemSchemaExtra):
    results = {"item_id": item_id, "item": item}
    return results


# Field additional arguments
# When using Field() with Pydantic models, you can also declare extra info for the JSON Schema
# by passing any other arbitrary arguments to the function. You can use this to add example for
# each field:
class ItemField(BaseModel):
    name: str = Field(..., example="Foo")
    description: Optional[str] = Field(None, example="A very nice Item")
    price: float = Field(..., example=35.4)
    tax: Optional[float] = Field(None, example=3.2)

@app.put("/items/field/{item_id}")
async def update_item(item_id: int, item: ItemField):
    results = {"item_id": item_id, "item": item}
    return results

# When using any of Path(), Query(), Header(), Cookie(), Body(), Form(), File() you can also declare a
# data example or a group of examples with additional information that will be added to OpenAPI.

# Body with example
# Here we pass an example of the data expected in Body():
class ItemBodyExample(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


@app.put("/items/body_example/{item_id}")
async def update_item(
    item_id: int,
    item: ItemBodyExample = Body(
        ...,
        example={
            "name": "Foo",
            "description": "A very nice Item",
            "price": 35.4,
            "tax": 3.2,
        },
    ),
):
    results = {"item_id": item_id, "item": item}
    return results


# Body with multiple examples
# Alternatively to the single example, you can pass examples using a dict with multiple examples, each with
# extra information that will be added to OpenAPI too.
# The keys of the dict identify each example, and each value is another dict.
# Each specific example dict in the examples can contain:
# - summary: Short description for the example.
# - description: A long description that can contain Markdown text.
# - value: This is the actual example shown, e.g. a dict.
# - externalValue: alternative to value, a URL pointing to the example. Although this might not be supported
# by as many tools as value.
class ItemMultipleExample(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

@app.put("/items/multiple_example/{item_id}")
async def update_item(
    *,
    item_id: int,
    item: ItemMultipleExample = Body(
        ...,
        examples={
            "normal": {
                "summary": "A normal example",
                "description": "A **normal** item works correctly.",
                "value": {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                },
            },
            "converted": {
                "summary": "An example with converted data",
                "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
                "value": {
                    "name": "Bar",
                    "price": "35.4",
                },
            },
            "invalid": {
                "summary": "Invalid data is rejected with an error",
                "value": {
                    "name": "Baz",
                    "price": "thirty five point four",
                },
            },
        },
    ),
):
    results = {"item_id": item_id, "item": item}
    return results

