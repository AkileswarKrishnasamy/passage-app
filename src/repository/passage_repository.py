from sqlalchemy.orm import Session
from models import Passage
from typing import List
from exceptions import DuplicateException, NotFoundException
from sqlalchemy.exc import SQLAlchemyError

class PassageRepository:
    def __init__(self,db:Session) -> None:
        self.db = db
    
    def get_all_passages(self) -> List[Passage]:
        """fetches all passages from passages table"""
        return self.db.query(Passage).all()

    def add_passage(self, passage: Passage) -> None:
        """Adds new passage to passages table"""
        try:

            self.db.add(passage)
            self.db.commit()
            self.db.refresh(passage)

        except SQLAlchemyError:

            self.db.rollback()
            raise
        

    def get_passage_by_id(self,user_id:int, passage_id: int) -> Passage:
        """fetches passage by id"""
        passage = self.db.query(Passage).filter(Passage.id == passage_id).filter(Passage.user_id == user_id).first()

        if passage is None:
            raise NotFoundException(detail='No passage found for given id')
        
        return passage  # type: ignore


    def get_passages_by_user_id(self, user_id: int) -> List[Passage]:
        """fetches all passages of user"""
        passages = self.db.query(Passage).filter(Passage.user_id == user_id).all()

        if passages == []:
            raise NotFoundException(detail='No passages found for given user')
        
        return passages # type: ignore

    def get_passages_by_author(self, author: str) -> List[Passage]:
        """fetches all passages of author"""

        passages = self.db.query(Passage).filter(Passage.author == author).all()

        if passages == []:
            raise NotFoundException(detail='No passages found for given author')
        
        return passages # type: ignore
    

    def get_passages_by_book(self, book: str) -> List[Passage]:
        """fetches all passages of book"""

        passages = self.db.query(Passage).filter(Passage.book == book).all()

        if passages == []:
            raise NotFoundException(detail='No passages found for given book')
        
        return passages # type: ignore

    def update_passage(self, passage_id: int, passage_str: str) -> None:
        """updates a passage"""
        try:
            passage = self.db.query(Passage).filter(Passage.id == passage_id).first()

            if passage is None:
                raise NotFoundException(detail='No passage found with given id')
            
            passage.passage = passage_str # type: ignore

            self.db.commit()
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def delete_passage(self,user_id: int, passage_id: int) -> None:
        """deletes a passage"""
        try:
            passage = self.db.query(Passage).filter(Passage.id == passage_id).filter(Passage.user_id == user_id).first()

            if passage is None:
                raise NotFoundException(detail='No passage found with given id')

            self.db.delete(passage)
            self.db.commit()
        except SQLAlchemyError:
            self.db.rollback()
            raise





