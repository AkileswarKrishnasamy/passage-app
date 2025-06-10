from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from config.database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    username = Column(String(100), nullable=False, unique=True, index=True)
    hash_password = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False)

    
