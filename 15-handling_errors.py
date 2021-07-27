# To run only this file with uvicorn use: uvicorn 15-handling_errors:app --reload
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel


# Create FastAPI instance
app = FastAPI()


# There are many situations in where you need to notify an error to a client that is using your API.
# You could need to tell the client that:
# - The client doesn't have enough privileges for that operation.
# - The client doesn't have access to that resource.
# - The item the client was trying to access doesn't exist.
# - etc.
# To return HTTP responses with errors to the client you use HTTPException.
items = {"foo": "The Foo Wrestlers"}

# HTTPException is a normal Python exception with additional data relevant for APIs.
# Because it's a Python exception, you don't return it, you raise it.
# When raising an HTTPException, you can pass any value that can be converted to JSON as the parameter
# detail, not only str.
@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": items[item_id]}


@app.get("/items-header/{item_id}")
async def read_item_header(item_id: str):
    if item_id not in items:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": "There goes my error"},
        )
    return {"item": items[item_id]}


# You can add custom exception handlers with the same exception utilities from Starlette.
# Let's say you have a custom exception UnicornException that you (or a library you use) might raise.
# And you want to handle this exception globally with FastAPI.
# You could add a custom exception handler with @app.exception_handler().
class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name

@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
    )

# Here, if you request /unicorns/yolo, the path operation will raise a UnicornException.
# But it will be handled by the unicorn_exception_handler
@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}


# FastAPI has some default exception handlers.
# These handlers are in charge of returning the default JSON responses when you raise an HTTPException
# and when the request has invalid data.
# You can override these exception handlers with your own.
# When a request contains invalid data, FastAPI internally raises a RequestValidationError.
# And it also includes a default exception handler for it.
# To override it, import the RequestValidationError and use it with @app.exception_handler(RequestValidationError)
# to decorate the exception handler. The exception handler will receive a Request and the exception.
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)

# The same way, you can override the HTTPException handler. For example, you could want to return a plain text response
# instead of JSON for these errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)

@app.get("/items_except/{item_id}")
async def read_item(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return {"item_id": item_id}


# The RequestValidationError contains the body it received with invalid data.
# You could use it while developing your app to log the body and debug it, return it to the user, etc.
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )

class Item(BaseModel):
    title: str
    size: int

@app.post("/items_err/")
async def create_item(item: Item):
    return item


'''
FastAPI has its own HTTPException.
And FastAPI's HTTPException error class inherits from Starlette's HTTPException error class.
The only difference, is that FastAPI's HTTPException allows you to add headers to be included in the response.
This is needed/used internally for OAuth 2.0 and some security utilities.
So, you can keep raising FastAPI's HTTPException as normally in your code.
But when you register an exception handler, you should register it for Starlette's HTTPException.
This way, if any part of Starlette's internal code, or a Starlette extension or plug-in, raises a Starlette HTTPException,
your handler will be able to catch and handle it.
In this example, to be able to have both HTTPExceptions in the same code, Starlette's exceptions is renamed to StarletteHTTPException.
'''
