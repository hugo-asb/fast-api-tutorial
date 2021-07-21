# To run only this file with uvicorn use: uvicorn 2-path_parameters:app --reload
from fastapi import FastAPI
from enum import Enum


# Create FastAPI instance
app = FastAPI()


# The value of the parameter {item_id} is passed to the function.
# Is possible to declare a type of this parameter.
@app.get("/item/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


# Path operations are evaluated in order, so ORDERS MATTERS.
# If we swap these two funcions, read_user_me would never be evoked, because
# read_user would be evaluated first.
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


# Enum class. Used to create attributes with fixed values.
class ModelName(str, Enum):
    alexnet = 'alexnet'
    resnet = 'resnet'
    lenet = 'lenet'

# Only the values defined on ModelName class would be valids.
@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:  # Compare the received parameter with the enumerator member in ModelName.
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    
    if model_name.value == "lenet":  # Compare the actual value of model_name with the string "lenet".
        return {"model_name": model_name, "message": "LeCNN all the images."}
    
    return {"model_name": model_name, "message": "Have some residuals."}  # Return enum member from path operation.


# Declare a path parameter containing a path using a URL. the name of the parameter
# is file_path, and the last part, :path, tells it that the parameter should match any path.
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}

