from fastapi import Header, HTTPException


'''
We see that we are going to need some dependencies used in several
places of the application.
So we put them in their own dependencies module (app/dependencies.py).
We will now use a simple dependency to read a custom X-Token header
'''

async def get_token_header(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def get_query_token(token: str):
    if token != "jessica":
        raise HTTPException(status_code=400, detail="No Jessica token provided")
