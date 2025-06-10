from pydantic import BaseModel

class UserBase(BaseModel):
    id: int
    email: str
    username: str
    password: str
    role: str


class UserCreate(BaseModel):
    email: str
    username: str
    password: str

class UserUpdate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

