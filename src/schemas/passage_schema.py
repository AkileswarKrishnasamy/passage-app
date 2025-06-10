from pydantic import BaseModel


class PassageCreate(BaseModel):
    passage: str
    book: str
    page_number: int
    author: str
    genre: str
    
class PassageUpdate(BaseModel):
    id: int
    passage: str

class PassageBase(BaseModel):
    
    id: int 
    passage: str
    book: str
    page_number: int
    author: str
    genre: str
    user_id: int