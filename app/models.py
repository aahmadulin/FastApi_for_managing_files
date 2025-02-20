from sqlalchemy import Column, Integer, String, Float
from .database import Base

# Класс для таблицы files
class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    size = Column(Float)
    format = Column(String)
    extension = Column(String)
    uid = Column(String, unique=True, index=True)