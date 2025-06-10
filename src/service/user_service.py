from sqlalchemy.orm import Session
from repository import UserRepository
from models import User
from schemas import UserCreate, UserUpdate, UserBase
from config import bcrypt_context
from typing import List



class UserService:
    def __init__(self,db:Session) -> None:
        self.user_repo = UserRepository(db)
    
    def create_new_user(self, user: UserCreate) -> None:
        
        hash_password = bcrypt_context.hash(user.password)
        db_user = User( email=user.email,username=user.username,
                       hash_password=hash_password,role='user') 
        self.user_repo.add_user(db_user)

    def get_user(self, user_id: int) -> UserBase: # type: ignore

        db_user = self.user_repo.get_user_by_id(user_id=user_id)
        return UserBase(**db_user.model_dump())

    def get_user(self, username: str) -> UserBase:

        db_user = self.user_repo.get_user_by_username(username=username)
        return UserBase(id = db_user.id, # type: ignore
                        email = db_user.email,  # type: ignore
                        username = db_user.username, # type: ignore
                        password= db_user.hash_password, # type: ignore
                        role = db_user.role) # type: ignore
    
    def update_user(self, user_upadate: UserUpdate) -> None:

        new_hash_password = bcrypt_context.hash(user_upadate.password)
        self.user_repo.update_user_password(username=user_upadate.username
                                            , new_hash_password=new_hash_password)

    def delete_user(self, user_id: int) -> None:
        self.user_repo.delete_user(user_id)

