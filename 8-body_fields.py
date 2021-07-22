# To run only this file with uvicorn use: uvicorn 8-body_fields:app --reload
from fastapi import Body, FastAPI
from pydantic import BaseModel, Field
from typing import Optional


# Create FastAPI instance
app = FastAPI()


# The same way you can declare additional validation and metadata in path operation function parameters
# with Query, Path and Body, you can declare validation and metadata inside of Pydantic models using
# Pydantic's Field.
class Item(BaseModel):
    name: str
    description: Optional[str] = Field(
        None, title="The description of the item", max_length=300
    )
    price: float = Field(..., gt=0, description="The price must be greater than zero")
    tax: Optional[float] = None

# Field works the same way as Query, Path and Body, it has all the same parameters, etc.
@app.put("/items/field/{item_id}")
async def update_item(item_id: int, item: Item = Body(..., embed=True)):
    results = {"item_id": item_id, "item": item}
    return results
