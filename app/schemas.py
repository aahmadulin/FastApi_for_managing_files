from pydantic import BaseModel

# Класс для описания файла
# pydantic использован для облегчения и правильной валидации...
class FileBase(BaseModel):
    filename: str
    size: float
    format: str
    extension: str
    uid: str

# Класс для создания файла (нужен для читаемости и будущего дополнения полей и логики)
class FileCreate(FileBase):
    pass

# Класс для представления файла, для возвращения данных о файле из API
class File(FileBase):
    id: int

    class Config:
        orm_mode = True