# To run only this file with uvicorn use: uvicorn 11-cookie_headers_parameters:app --reload
from fastapi import FastAPI, Cookie, Header
from typing import Optional, List


# Create FastAPI instance
app = FastAPI()


# Cookie parameters are declared using the same structure as with Path and Query.
# Cookie is a "sister" class of Path, Query and Header. It also inherits from the
# same common Param class.
# When you import Query, Path, Cookie and others from fastapi, those are actually
# functions that  return special classes.
@app.get("/items/cookies/")
async def read_items(ads_id: Optional[str] = Cookie(None)):
    return {"ads_id": ads_id}


# Header parameters are declared using the same structure as with Path, Query and Cookie.
# The first value is the default value, you can pass all the extra validation or annotation
# parameters.
@app.get("/items/header/")
async def read_items(user_agent: Optional[str] = Header(None)):
    return {"User-Agent": user_agent}

# Header has a little extra functionality on top of what Path, Query and Cookie provide.
# Most of the standard headers are separated by a "hyphen" character (-). but a variable
# like user-agent is invalid in Python. So, by default, Header will convert the parameter names
# characters from underscore (_) to hyphen (-) to extract and document the headers.
# HTTP headers are case-insensitive, so, you can declare them with standard Python style ("snake_case").
# You can use user_agent as you normally would in Python code, instead of needing to capitalize the
# first letters as User_Agent or something similar.
# Set the parameter convert_underscores of Header to False to disable this kind of conversion.
# Obs.: some HTTP proxies and servers disallow the usage of headers with underscores.
@app.get("/items/header_convert_/")
async def read_items(
    strange_header: Optional[str] = Header(None, convert_underscores=False)):
    return {"strange_header": strange_header}

# It is possible to receive duplicate headers. That means, the same header with multiple values.
# You can define those cases using a list in the type declaration.
# You will receive all the values from the duplicate header as a Python list.
@app.get("/items/header_duplicate/")
async def read_items(x_token: Optional[List[str]] = Header(None)):
    return {"X-Token values": x_token}
