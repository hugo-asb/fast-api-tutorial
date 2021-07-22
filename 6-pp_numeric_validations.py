# pp = Path Parameters
# To run only this file with uvicorn use: uvicorn 6-pp_numeric_validatios:app --reload
from fastapi import FastAPI, Query, Path
from typing import Optional


# Create FastAPI instance
app = FastAPI()


# As for query parameters, it's possible to declare the same type of validations and metadata
# for path parameters with Path. A path parameter is always required as it has to be part of
# the path, so, you should declare it with ... to mark it as required. even if you declared
# it with None or set a default value, it would not affect anything, it would still be always required.
@app.get("/items/p_prms/{item_id}")
async def read_items(
    item_id: int = Path(..., title="The ID of the item to get"),
    q: Optional[str] = Query(None, alias="item-query"),
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

# FastAPI will detect the parameters by their names, types and default declarations (Query, Path, etc),
# it doesn't care about the order. In this case, Python would complain if you put a value with a "default"
# before a value that doesn't have a "default". So, you can re-order them, and have the value without a
# default (the query parameter q) first.
@app.get("/items/prms_order/{item_id}")
async def read_items(
    q: str, item_id: int = Path(..., title="The ID of the item to get")
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

# If you want to declare the q query parameter without a Query nor any default value, and the path parameter
# item_id using Path, and have them in a different order, pass * as the first parameter of the function.
@app.get("/items/kwargs/{item_id}")
async def read_items(
    *, item_id: int = Path(..., title="The ID of the item to get"), q: str
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

# The same way it's possible to declare string constraints, you can also do number constraints.
@app.get("/items/int_valid/{item_id}")
async def read_items(
    *,
    item_id: int = Path(..., title="The ID of the item to get", gt=0, le=1000),
    q: str,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

# Number validations also work for float values.
@app.get("/items/float_valid/{item_id}")
async def read_items(
    *,
    item_id: int = Path(..., title="The ID of the item to get", ge=0, le=1000),
    q: str,
    size: float = Query(..., gt=0, lt=10.5)
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


'''
When you import Query, Path and others from fastapi, they are actually functions.

That when called, return instances of classes of the same name.

So, you import Query, which is a function. And when you call it, it returns an instance
of a class also named Query.

These functions are there (instead of just using the classes directly) so that your editor
doesn't mark errors about their types.

That way you can use your normal editor and coding tools without having to add custom configurations
to disregard those errors.
'''
