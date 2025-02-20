from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles  # Импортируем StaticFiles
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, crud
from .database import SessionLocal, engine
import os
import uuid

# Создание таблиц в БД
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Статические файлы для фронта
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Зависимость для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db # Приостановление после создания сессии, чтобы затем корректно завершить сессию
    finally:
        db.close()

# Эндпоинт для загрузки файла
@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Генерация UID
    file_uuid = str(uuid.uuid4())
    # Сохраняем файл на сервере
    file_location = f"app/static/uploads/{file_uuid}_{file.filename}"
    # Создаем директорию, если она не существует
    os.makedirs(os.path.dirname(file_location), exist_ok=True)
    
    # Записываем файл
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
    
    # Создаем метаданные файла
    file_metadata = schemas.FileCreate(
        filename=file.filename,
        size=os.path.getsize(file_location),
        format=file.content_type,
        extension=os.path.splitext(file.filename)[1],
        uid=file_uuid
    )
    
    # Сохраняем метаданные в БД
    return crud.create_file(db=db, file=file_metadata)

# Эндпоинт для получения списка файлов
@app.get("/files/", response_model=List[schemas.File])
def read_files(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    files = crud.get_files(db, skip=skip, limit=limit)
    return files

# Эндпоинт для получения файла по его UID (ТОЛЬКО ПО UID, не по ID)
@app.get("/files/{file_id}", response_model=schemas.File)
def read_file(file_id: str, db: Session = Depends(get_db)):
    db_file = crud.get_file(db, file_id=file_id)
    if db_file is None:
        raise HTTPException(status_code=404, detail="File not found")
    return db_file

# Фронт для загрузки файлов
@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("frontend/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())