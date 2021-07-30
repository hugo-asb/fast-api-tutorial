from fastapi import APIRouter

'''
Let's say the file dedicated to handling just users is the submodule
at /app/routers/users.py.
You want to have the path operations related to your users separated
from the rest of the code, to keep it organized.
But it's still part of the same FastAPI application/web API (it's part
of the same "Python Package").
You can create the path operations for that module using APIRouter.

You can think of APIRouter as a "mini FastAPI" class.
All the same options are supported.
All the same parameters, responses, dependencies, tags, etc.
'''

# Import it and create an "instance" the same way you would with the class FastAPI.
router = APIRouter()


@router.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/users/me", tags=["users"])
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}