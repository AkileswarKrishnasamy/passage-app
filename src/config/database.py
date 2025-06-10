from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os 
from dotenv import load_dotenv

load_dotenv()
ROOT = os.getenv('DATABASE_USERNAME')
PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE = os.getenv('DATABASE_NAME')
PORT = os.getenv('DATABASE_PORT')

SQL_DB_URL = f"mysql+mysqldb://{ROOT}:{PASSWORD}@localhost:{PORT}/{DATABASE}"

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

