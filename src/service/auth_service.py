from repository import UserRepository
from sqlalchemy.orm import Session
from config import bcrypt_context
from schemas import UserLogin
import os
from dotenv import load_dotenv
import jwt
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from typing import List
from fastapi.responses import JSONResponse

load_dotenv()

class AuthService:

    def __init__(self, db: Session) -> None:
        
        self.exp_delta = 30 * 60 #30 minutes
        self.ref_exp_delta = 30 * 34 * 60 * 60 #30 days
        self.secret = os.getenv("SECRET_KEY")
        self.algorithm = os.getenv("ALGORITHM")
        self.user_repo = UserRepository(db)

    def validate_user(self, username: str, password: str) -> bool:

        user = self.user_repo.get_user_by_username(username)
        return bcrypt_context.verify(password, user.hash_password) # type: ignore
    

    
    
    def _generate_tokens(self, username: str, user_id: int,role: str) -> List[str]:

        expiration_time = datetime.now(timezone.utc) + timedelta(seconds=self.exp_delta)
        payload = {
            'user': username,
            'id': user_id,
            'role': role,
            'exp': expiration_time
        }
        
        access_token =  jwt.encode(payload,self.secret,self.algorithm)

        expiration_time = datetime.now(timezone.utc) + timedelta(seconds=self.ref_exp_delta)
        payload = {
            'user': username,
            'id': user_id,
            'role': role,
            'exp': expiration_time
        }

        refresh_token =  jwt.encode(payload,self.secret,self.algorithm)

        return [access_token, refresh_token]
        
    def sign_in_user(self, credentials: UserLogin) -> List[str]:

        if self.validate_user(credentials.username, credentials.password):
            user = self.user_repo.get_user_by_username(credentials.username)
            print(f'username:{user.username} password:{user.hash_password} role:{user.role}')
            return self._generate_tokens(user.username, user.id, user.role) # type: ignore
        else:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail='Invalid Credentials')
        
    def refresh_token(self, refresh_token: str) -> List[str]:

        if not refresh_token:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='No refresh token')
        
        try:
        
            payload = jwt.decode(refresh_token,key=self.secret,algorithms = [self.algorithm] ) # type: ignore
            
            user = self.user_repo.get_user_by_username(payload.get('user'))
            if user:
                return self._generate_tokens(user.username,user.id,user.role) # type: ignore       
            else :
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token Invalid')
            
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid refresh token')
        
        


