from pydantic import BaseModel
from datetime import datetime 

class PostBase(BaseModel):      #defining expected input
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):     #inherits properties of postbase
    pass

class Post(PostBase):           #making response model
    id: int
    created_at: datetime

    class Config:
        orm_mode = True         #tell the Pydantic model to read the data even if it is not a dict, but an ORM model (or any other arbitrary object with attributes)