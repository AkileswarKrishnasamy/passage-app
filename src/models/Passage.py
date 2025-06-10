from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base
from config.database import Base


class Passage(Base):
    __tablename__ = 'passages'

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    passage = Column(String(5000), nullable=False)
    book = Column(String(250))
    page_number = Column(Integer, nullable=False)
    author = Column(String(50))
    genre = Column(String(50))

    user_id = Column(Integer, ForeignKey('users.id'))
