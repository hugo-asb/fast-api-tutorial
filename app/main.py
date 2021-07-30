from fastapi import Depends, FastAPI

from .dependencies import get_query_token, get_token_header
from .internal import admin
from .routers import items, users


'''
You import and create a FastAPI class as normally.
And we can even declare global dependencies that will be combined with
the dependencies for each APIRouter
'''

app = FastAPI(dependencies=[Depends(get_query_token)])


'''
We are importing the submodule items directly, instead of importing just its variable router.
This is because we also have another variable named router in the submodule users.
If we had imported one after the other, the router from users would overwrite the one from items
and we wouldn't be able to use them at the same time.
So, to be able to use both of them in the same file, we import the submodules directly.

Now, let's imagine your organization gave you the app/internal/admin.py file. It contains an APIRouter
with some admin path operations that your organization shares between several projects.
Let's say that because it is shared with other projects in the organization, we cannot modify it and add
a prefix, dependencies, tags, etc. directly to the APIRouter.
We can declare all that without having to modify the original APIRouter by passing those parameters to
app.include_router().
That way, the original APIRouter will keep unmodified, so we can still share that same app/internal/admin.py
file with other projects in the organization. The result is that in our app, each of the path operations from
the admin module will have:
- The prefix /admin.
- The tag admin.
- The dependency get_token_header.
- The response 418.
But that will only affect that APIRouter in our app, not in any other code that uses it.
So, for example, other projects could use the same APIRouter with a different authentication method.
'''
app.include_router(users.router)
app.include_router(items.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)


# We can also add path operations directly to the FastAPI app and it will work correctly, together with all the
# other path operations added with app.include_router().
@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
