from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from models import User
from passlib.context import CryptContext
from typing import List
from exceptions import NotFoundException, DuplicateException

bcrypt_context = CryptContext(schemes=['bcrypt'])

class UserRepository:
    def __init__(self,db:Session) -> None:
        self.db = db
    
    def get_all_users(self) -> List[User]:
        """fetches all users from the database"""
        users = self.db.query(User).filter(User.role == 'user')

        if not users:
            raise NotFoundException('No data found')
        return users # type: ignore
    
    def get_all_admin(self) -> List[User]:
        """fetches all users from the database"""
        admins = self.db.query(User).filter(User.role == 'admin')

        if not admins:
            raise NotFoundException('No data found')
        
        return admins # type: ignore
    

    def add_user(self,user: User)->None:
        """Adds user to the users table"""
        try:
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
        except IntegrityError as e:
            self.db.rollback()
            raise DuplicateException(detail='User Already exist')
        

    def get_user_by_id(self,user_id: int) -> User:
        """fetches user with user id"""

        user = self.db.query(User).filter(User.id == user_id).first()

        if user is None:
            raise NotFoundException(detail='No user found with given id')
        
        return user
  
    
    def get_user_by_username(self,username: str) -> User:
        """fetches user with username"""
        user = self.db.query(User).filter(User.username == username).first()

        if user is None:
            raise NotFoundException(detail='No user found with given username')
        
        return user


    def update_user_password(self,username: str,new_hash_password: str):
        """updates the password of the user. provide hashed password """
        try:
            user = self.db.query(User).filter(User.username == username).first()

            if user is None:
                raise NotFoundException(detail='No user found with given username')
            
            user.hash_password = new_hash_password # type: ignore
            self.db.commit()
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def delete_user(self, user_id: int) -> None:
        """deletes user from the users table"""
        try:
            user = self.db.query(User).filter(User.id == user_id).first()

            if user is None:
                raise NotFoundException(detail='No user found with given id')
            
            self.db.delete(user)
            self.db.commit()

        except SQLAlchemyError:
            self.db.rollback()
            raise

        
