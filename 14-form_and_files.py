# To run only this file with uvicorn use: uvicorn 14-form_and_files:app --reload
from fastapi import FastAPI, Form, File, UploadFile
from fastapi.responses import HTMLResponse
from typing import List


# Create FastAPI instance
app = FastAPI()


# Form is used to receive form fields instead of JSON.
# With Form you can declare the same metadata and validation as with Body, Query, Path, etc.
@app.post("/login/")
async def login(username: str = Form(...), password: str = Form(...)):
    return {"username": username}


# File is used to define files to be uploaded by the client.
# Uploaded files are sent as form data.
# With File you can declare the same metadata and validation as with Body, Query, Path, etc.
# If you declare the type of your path operation function parameter as bytes, FastAPI will read
# the file for you and you will receive the contents as bytes. So, the whole contents will be stored
# in memory. This will work well for small files.
@app.post("/files/")
async def create_file(file: bytes = File(...)):
    return {"file_size": len(file)}

# UploadFile has several advantages over bytes:
# - It uses a "spooled" file (a file stored in memory up to a maximum size limit, and after passing this
# limit it will be stored in disk - it will work well for large files without consuming all the memory.
# - You can get metadata from the uploaded file.
# - It has a file-like async interface.
# - It exposes an actual Python SpooledTemporaryFile object that you can pass directly to other libraries
# that expect a file-like object.
@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename, "content-type": file.content_type}

# It's possible to upload several files at the same time. They would be associated to the same "form field"
# sent using "form data". To use that, declare a List of bytes or UploadFile.
@app.post("/many_files/")
async def create_files(files: List[bytes] = File(...)):
    return {"file_sizes": [len(file) for file in files]}

@app.post("/many_uploadfiles/")
async def create_upload_files(files: List[UploadFile] = File(...)):
    return {"filenames": [file.filename for file in files]}

@app.get("/")
async def main():
    content = """
<body>
<form action="/many_files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/many_uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)


# It is possible to define files and form fields at the same time.
# The files and form fields will be uploaded as form data and you will receive the files and form fields,
# and you can declare some of the files as bytes and some as UploadFile.
# You can't also declare Body fields that you expect to receive as JSON, as the request will have the body
# encoded using multipart/form-data instead of application/json (this is part of the HTTP protocol). 
@app.post("/form_files/")
async def create_file(
    file: bytes = File(...), fileb: UploadFile = File(...), token: str = Form(...)
):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
    }
