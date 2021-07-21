# qp = Query Parameters
# To run only this file with uvicorn use: uvicorn 5-qp_string_validatios:app --reload
from fastapi import FastAPI, Query
from typing import Optional, List


# Create FastAPI instance
app = FastAPI()


# The query parameter q is of type Optional[str], that means that it's of type str but could
# also be None, and indeed, the default value is None, so FastAPI will know it's not required.
@app.get("/items/")
async def read_items(q: Optional[str] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# Even though q is optional, whenever it is provided, its length doesn't exceed 50 characters 
# and have at least 3 characters.
# ^: checks if starts with the following characters, doesn't have characters before.
# fixedquery: has the exact value fixedquery.
# $: ends there, doesn't have any more characters after fixedquery.
@app.get("/items/validation/")
async def read_items(q: Optional[str] = Query(None,
                                              min_length=3,
                                              max_length=50,
                                              regex="^fixedquery$")
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# The same way that you can pass None as the first argument to be used as the default value,
# you can pass other values.
@app.get("/items/default/")
async def read_items(q: str = Query("fixedquery", min_length=3)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# To declare a value as required while using Query, you can use ... as the first argument
@app.get("/items/required/")
async def read_items(q: str = Query(..., min_length=3)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# When you define a query parameter explicitly with Query you can also declare it to receive a
# list of values, or said in other way, to receive multiple values.
# Path example: /items/list/?q=foo&q=bar&q=let&q=try
@app.get("/items/list/")
async def read_items(q: Optional[List[str]] = Query(None)):
    query_items = {"q": q}
    return query_items

# You can add more information about the parameter. That information will be included in the generated
# OpenAPI and used by the documentation user interfaces and external tools.
@app.get("/items/metadata/")
async def read_items(
    q: Optional[str] = Query(
        None,
        title="Query string",
        description="Query string for the items to search in the database that have a good match",
        min_length=3,
    )
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# Alias is used to find the parameter value. In this case, instead of the path receive q as a query parameter, 
# it will receive item-query. E.g. /items/alias?item-query=something
@app.get("/items/alias/")
async def read_items(q: Optional[str] = Query(None, alias="item-query")):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# If there is a parameter that is no longer in use, but you have to leave it there a while because there are
# clients using it and you want the docs to clearly show it as deprecated, just pass the parameter
# deprecated=True to Query
@app.get("/items/deprecated/")
async def read_items(
    q: Optional[str] = Query(
        None,
        alias="item-query",
        title="Query string",
        description="Query string for the items to search in the database that have a good match",
        min_length=3,
        max_length=50,
        regex="^fixedquery$",
        deprecated=True,
    )
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

