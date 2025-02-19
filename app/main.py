from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, crud
from .database import SessionLocal, engine
import os
import uuid

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_uuid = str(uuid.uuid4())
    file_location = f"app/static/uploads/{file_uuid}_{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
    
    file_metadata = schemas.FileCreate(
        filename=file.filename,
        size=os.path.getsize(file_location),
        format=file.content_type,
        extension=os.path.splitext(file.filename)[1],
        uid=file_uuid
    )
    
    return crud.create_file(db=db, file=file_metadata)

@app.get("/files/", response_model=List[schemas.File])
def read_files(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    files = crud.get_files(db, skip=skip, limit=limit)
    return files

@app.get("/files/{file_id}", response_model=schemas.File)
def read_file(file_id: str, db: Session = Depends(get_db)):
    db_file = crud.get_file(db, file_id=file_id)
    if db_file is None:
        raise HTTPException(status_code=404, detail="File not found")
    return db_file

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <html>
        <body>
            <form action="/uploadfile/" enctype="multipart/form-data" method="post">
                <input name="file" type="file">
                <input type="submit">
            </form>
        </body>
    </html>
    """