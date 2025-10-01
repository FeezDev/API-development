
from datetime import datetime
# from sqlalchemy import String
from pydantic import BaseModel, EmailStr


# handles sending data to the user
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None

# class Create_Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True
    class Config:  
        from_attribute = True


# we can just extent the postbase by:
class PostCreate(PostBase):
    pass

    class Config:
        from_attribute = True


# handling recieving data from user
class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        from_attribute = True


class UserCreate(BaseModel): 
    email: EmailStr
    password: str
    
    class Config:   
        from_attribute = True


class UserOut(BaseModel):
    id: int
    email: EmailStr
    
    class Config:
        from_attribute = True
