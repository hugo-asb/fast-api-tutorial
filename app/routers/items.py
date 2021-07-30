from fastapi import APIRouter, Depends, HTTPException

from ..dependencies import get_token_header


'''
We know all the path operations in this module have the same:
- Path prefix: /items.
- tags: (just one tag: items).
- Extra responses.
- dependencies: they all need that X-Token dependency we created.
So, instead of adding all that to each path operation, we can add it to the APIRouter.
The path of each path operation has to start with / and the prefix must not include a final /.

We can also add a list of tags and extra responses that will be applied to all the path
operations included in this router.
And we can add a list of dependencies that will be added to all the path operations in the
router and will be executed/solved for each request made to them.
'''

router = APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


fake_items_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}


@router.get("/")
async def read_items():
    return fake_items_db


@router.get("/{item_id}")
async def read_item(item_id: str):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"name": fake_items_db[item_id]["name"], "item_id": item_id}


@router.put(
    "/{item_id}",
    tags=["custom"],  # This will have the combination of tags: ["items", "custom"].
    responses={403: {"description": "Operation forbidden"}},  # Will have both responses in the documentation, one for 404 and one for 403.
)
async def update_item(item_id: str):
    if item_id != "plumbus":
        raise HTTPException(
            status_code=403, detail="You can only update the item: plumbus"
        )
    return {"item_id": item_id, "name": "The great Plumbus"}
