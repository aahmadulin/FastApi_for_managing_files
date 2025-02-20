from sqlalchemy.orm import Session
from . import models, schemas

def create_file(db: Session, file: schemas.FileCreate):
    db_file = models.File(**file.dict())
    # Добавляем, сохраняем, обновляем файлы в БД
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file

# Поиск файла в БД по его UID
def get_file(db: Session, file_id: str):
    return db.query(models.File).filter(models.File.uid == file_id).first()

# Получаем список файлов из БД. Можем пропустить сколько-то файлов или вернуть сколько-то файлов
def get_files(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.File).offset(skip).limit(limit).all()