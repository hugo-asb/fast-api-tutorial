# To run only this file with uvicorn use: uvicorn 17-dependencies:app --reload
from fastapi import FastAPI, Depends, Cookie, Header, HTTPException
from typing import Optional


app = FastAPI()


# "Dependency Injection" means that there is a way for your code (in this case, the path operation
# functions) to declare things that it requires to work and use: "dependencies".
# And then, that system will take care of doing whatever is needed to provide your code with those
# needed dependencies ("inject" the dependencies).
# This is very useful when you need to:
# - Have shared logic (the same code logic again and again).
# - Share database connections.
# - Enforce security, authentication, role requirements, etc.
# - And many other things.
# All these, while minimizing code repetition.
async def common_parameters(q: Optional[str] = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

# In this case, this dependency expects:
# - An optional query parameter q that is a str.
# - An optional query parameter skip that is an int, and by default is 0.
# - An optional query parameter limit that is an int, and by default is 100.
# - And then it just returns a dict containing those values.
@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons

# The same way you use Body, Query, etc. with your path operation function parameters, use Depends with
# a new parameter.
@app.get("/users/")
async def read_users(commons: dict = Depends(common_parameters)):
    return commons


# The key factor is that a dependency should be a "callable".
# A "callable" in Python is anything that Python can "call" like a function.
# So, if you have an object 'something' (that might not be a function) and you can "call" it (execute it),
# like 'something(argument)', then it is "callable".
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

# What FastAPI actually checks is that it is a "callable" (function, class or anything else) and the parameters
# defined. If you pass a "callable" as a dependency in FastAPI, it will analyze the parameters for that "callable",
# and process them in the same way as the parameters for a path operation function. Including sub-dependencies.
# That also applies to callables with no parameters at all, as it would be for path operation functions with no parameters.
class CommonQueryParams:
    def __init__(self, q: Optional[str] = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit

# FastAPI calls the CommonQueryParams class. This creates an "instance" of that class and the instance will be passed as
# the parameter commons to your function.
@app.get("/items/class/")
async def read_items(commons: CommonQueryParams = Depends(CommonQueryParams)):  # commons: CommonQueryParams = Depends()
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = fake_items_db[commons.skip : commons.skip + commons.limit]
    response.update({"items": items})
    return response


# You can create dependencies that have sub-dependencies. They can be as deep as you need them to be. FastAPI will take care
# of solving them.
def query_extractor(q: Optional[str] = None):
    return q

# Even though this function is a dependency ("dependable") itself, it also declares another dependency (it "depends" on something else).
# It depends on the query_extractor, and assigns the value returned by it to the parameter q.
# It also declares an optional last_query cookie, as a str.
# If the user didn't provide any query q, we use the last query used, which we saved to a cookie before.
def query_or_cookie_extractor(
    q: str = Depends(query_extractor), last_query: Optional[str] = Cookie(None)
):
    if not q:
        return last_query
    return q

@app.get("/items/sub/")
async def read_query(query_or_default: str = Depends(query_or_cookie_extractor)):
    return {"q_or_cookie": query_or_default}


# In some cases you don't really need the return value of a dependency inside your path operation function, or the dependency
# doesn't return a value. But you still need it to be executed/solved. For those cases, instead of declaring a path operation
# function parameter with Depends, you can add a list of dependencies to the path operation decorator.
# These dependencies can raise exceptions.
async def verify_token(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")

# They can declare request requirements (like headers) or other sub-dependencies.
# These dependencies can return values or not.
async def verify_key(x_key: str = Header(...)):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key

# These dependencies will be executed/solved the same way normal dependencies. But their value (if they return any) won't be
# passed to your path operation function. So, you can re-use a normal dependency (that returns a value) you already use somewhere else.
@app.get("/items/", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items():
    return [{"item": "Foo"}, {"item": "Bar"}]


'''
For some types of applications you might want to add dependencies to the whole application.
Similar to the way you can add dependencies to the path operation decorators, you can add them to the FastAPI application.
In that case, they will be applied to all the path operations in the application.

app = FastAPI(dependencies=[Depends(verify_token), Depends(verify_key)])

@app.get("/items/")
async def read_items():
    return [{"item": "Portal Gun"}, {"item": "Plumbus"}]

@app.get("/users/")
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]
'''


'''
FastAPI supports dependencies that do some extra steps after finishing. To do this, use yield instead of return, and write
the extra steps after (you need to use Python 3.7 or above, or in Python 3.6, install the "backports"). Make sure to use
yield one single time.

If you use a try block in a dependency with yield, you'll receive any exception that was thrown when using the dependency.
So, you can look for that specific exception inside the dependency with except SomeException.
In the same way, you can use finally to make sure the exit steps are executed, no matter if there was an exception or not.

async def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()

You can have sub-dependencies and "trees" of sub-dependencies of any size and shape, and any or all of them can use yield.
FastAPI will make sure that the "exit code" in each dependency with yield is run in the correct order.
For example, dependency_c can have a dependency on dependency_b, and dependency_b on dependency_a.

async def dependency_a():
    dep_a = generate_dep_a()
    try:
        yield dep_a
    finally:
        dep_a.close()

async def dependency_b(dep_a=Depends(dependency_a)):
    dep_b = generate_dep_b()
    try:
        yield dep_b
    finally:
        dep_b.close(dep_a)

async def dependency_c(dep_b=Depends(dependency_b)):
    dep_c = generate_dep_c()
    try:
        yield dep_c
    finally:
        dep_c.close(dep_b)

In this case dependency_c, to execute its exit code, needs the value from dependency_b (here named dep_b) to still be available.
And, in turn, dependency_b needs the value from dependency_a (here named dep_a) to be available for its exit code.

In Python, you can create Context Managers by creating a class with two methods: __enter__() and __exit__().
You can also use them inside of FastAPI dependencies with yield by using with or async with statements inside of the
dependency function:

class MySuperContextManager:
    def __init__(self):
        self.db = DBSession()

    def __enter__(self):
        return self.db

    def __exit__(self, exc_type, exc_value, traceback):
        self.db.close()

async def get_db():
    with MySuperContextManager() as db:
        yield db

When you create a dependency with yield, FastAPI will internally convert it to a context manager, and combine it with some
other related tools.
'''
