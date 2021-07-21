# To run only this file with uvicorn use: uvicorn 1-first_steps:app --reload
from fastapi import FastAPI


# Create FastAPI instance
app = FastAPI()


# Simple path operator. Decorator of FastAPI (path=/ e operation=get).
# Below is the function called when the path is evoked.
@app.get("/")
async def root():
    return {"message": "Hello World!"}