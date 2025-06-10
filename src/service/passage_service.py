from sqlalchemy.orm import Session
from repository import PassageRepository
from schemas import PassageBase, PassageCreate, PassageUpdate
from models import Passage
from typing import List

class PassageService:
    def __init__(self, db: Session) -> None:
        self.passage_repo = PassageRepository(db)
    
    def convert_db_passage_to_passage_base(self,db_passages: List[Passage]) -> List[PassageBase]: # type: ignore
        user_passages : List[PassageBase] = []
        for passage in db_passages:
         user_passages.append(PassageBase(
            id=passage.id, # type: ignore
            passage=passage.passage,  # type: ignore
            book=passage.book, # type: ignore
            page_number=passage.page_number, # type: ignore
            author=passage.author, # type: ignore
            genre=passage.genre, # type: ignore
            user_id=passage.user_id # type: ignore
        )) 
         
        return user_passages
    
    def get_all_passages(self):

        db_passages = self.passage_repo.get_all_passages()
        return self.convert_db_passage_to_passage_base(db_passages)

    def add_new_passage(self, user_id: int, new_passage: PassageCreate) -> None:

        db_passage = Passage(**new_passage.model_dump(), user_id=user_id)
        self.passage_repo.add_passage(db_passage)

    def get_passage_by_id(self,user_id:int, passage_id: int) -> PassageBase:

        db_passage = self.passage_repo.get_passage_by_id(user_id,passage_id)

        return PassageBase(
            id=db_passage.id, # type: ignore
            passage=db_passage.passage,  # type: ignore
            book=db_passage.book, # type: ignore
            page_number=db_passage.page_number, # type: ignore
            author=db_passage.author, # type: ignore
            genre=db_passage.genre, # type: ignore
            user_id=db_passage.user_id # type: ignore
        ) 

    def get_passage_by_user_id(self, user_id: int) -> List[PassageBase]: 

        db_user_passages = self.passage_repo.get_passages_by_user_id(user_id=user_id)
        return self.convert_db_passage_to_passage_base(db_passages=db_user_passages)
    
    def get_passage_by_author(self, author: str) -> List[PassageBase]: 

        db_user_passages = self.passage_repo.get_passages_by_author(author=author)
        return self.convert_db_passage_to_passage_base(db_passages=db_user_passages)
    
    def get_passage_by_book(self, book: str) -> List[PassageBase]: 

        db_user_passages = self.passage_repo.get_passages_by_book(book=book)
        return self.convert_db_passage_to_passage_base(db_passages=db_user_passages)
    
    def update_passage(self, passage: PassageUpdate) -> None:

        self.passage_repo.update_passage(passage_id=passage.id, passage_str=passage.passage)

    def delete_passage(self,user_id:int, passage_id: int) -> None:

        self.passage_repo.delete_passage(user_id,passage_id)