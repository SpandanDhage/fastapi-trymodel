from typing import List, Optional
from pydantic import BaseModel


class BlogBase(BaseModel):
    title:str
    body:str

class Blog(BlogBase):
    userId:str
    class Config():
        orm_mode=True


class User(BaseModel):
    name:str
    email:str
    password: str

class showUser(BaseModel):
    name: str
    email: str
    blog: List[Blog]=[]
    class Config():
        orm_mode=True

class showUser1(BaseModel):
    name: str
    email: str
    class Config():
        orm_mode=True

class showBlog(Blog):
    creator:showUser1
    class Config():
        orm_mode=True

class Login(BaseModel):
    username:str=None
    password:str=None

class Token(BaseModel):
    access_token: str
    token_type : str

class TokenData(BaseModel):
    username: Optional[str]=None