from pydantic import BaseModel, EmailStr
from datetime import datetime 
from typing import Optional

class PostBase(BaseModel):      #defining expected input
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):     #inherits properties of postbase
    pass

class Post(PostBase):           #making response model
    id: int
    created_at: datetime
    owner_id: int

    class Config:
        orm_mode = True         #tell the Pydantic model to read the data even if it is not a dict, but an ORM model (or any other arbitrary object with attributes)

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None