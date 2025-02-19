from pydantic import BaseModel

class FileBase(BaseModel):
    filename: str
    size: float
    format: str
    extension: str
    uid: str

class FileCreate(FileBase):
    pass

class File(FileBase):
    id: int

    class Config:
        orm_mode = True