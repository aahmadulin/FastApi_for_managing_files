from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Пароль: 123456, Порт: 5432, username: postgres 
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:123456@localhost:5432/media_db" 
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()