from sqlalchemy.orm import Session
from repository import UserRepository, PassageRepository
from typing import List
from schemas import UserBase,UserCreate
from models import User
from schemas import PassageBase
from config import bcrypt_context

class AdminService:
    def __init__(self, db: Session) -> None:
        self.user_repo = UserRepository(db=db)
        self.passage_repo = PassageRepository(db=db)
    
    def convert_db_user_to_user_base(self, db_users: List[User]) -> List[UserBase]:

        users: List[UserBase] = []
        for user in db_users:
            users.append(
                UserBase(
                    id = user.id, # type: ignore
                    email= user.email, # type: ignore
                    username=user.username, # type: ignore
                    password=user.hash_password, # type: ignore
                    role=user.role # type: ignore
                )
            )
        
        return users
    
    def add_new_admin(self, admin: UserCreate) -> None:
        db_admin = User(
            username = admin.username,
            email = admin.email,
            hash_password = bcrypt_context.hash(admin.password),
            role = 'admin'
        )

        self.user_repo.add_user(db_admin)

    def get_all_users(self) -> List[UserBase]:

        db_users = self.user_repo.get_all_users()
        return self.convert_db_user_to_user_base(db_users=db_users)
    
    def get_all_admins(self) -> List[UserBase]:

        db_admins = self.user_repo.get_all_admin()
        return self.convert_db_user_to_user_base(db_users=db_admins)
    
    def get_all_passages(self) -> List[PassageBase]:

        db_passages = self.passage_repo.get_all_passages()
        passages = []
        for passage in db_passages:
            passages.append(
                PassageBase(
                    id = passage.id, # type: ignore
                    passage = passage.passage, # type: ignore
                    book = passage.book, # type: ignore
                    author=passage.author, # type: ignore
                    page_number=passage.page_number, # type: ignore
                    genre=passage.genre, # type: ignore
                    user_id=passage.user_id # type: ignore
                ) # type: ignore
            )
        
        return passages

    
