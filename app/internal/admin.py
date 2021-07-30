# Some administrative code here.
from fastapi import APIRouter


router = APIRouter()


@router.get("/admin/")
async def read_admin():
    return {"admin": "Some admin stuff."}
