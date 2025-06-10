from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os 
from dotenv import load_dotenv

load_dotenv()


SQL_DB_URL = f'{os.getenv('DB_URL')}'

engine = create_engine(SQL_DB_URL) 
session_local = sessionmaker(autocommit = False, autoflush= False, bind=engine)

Base = declarative_base()

from models import Passage,User
Base.metadata.create_all(engine)


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

