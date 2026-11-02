from pydantic import BaseModel, EmailStr,ConfigDict
from datetime import datetime
from typing import Optional

#from fastapi.params import Body
# from pydantic import BaseModel
# class Post(BaseModel):
#     title: str
#     content: str

class CreateUser(BaseModel):
    email:EmailStr
    password:str
class UserResponse(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime
    model_config=ConfigDict(from_attributes=True)
    # class config:# here during response object is from sqlalchemy so pydantic basemodel donot what to do so we have to configure orm = true
    #     orm_mode=True 
class UserLogin(BaseModel):
    email:EmailStr
    password:str

class PostBase(BaseModel):
    title:str
    id:int|None=None
    inventory:int|None=None
    created_at:datetime|None=None
   
class CreatePost(BaseModel):
    title:str
    content:str
    id:int|None=None
    inventory:int|None=None
    created_at:datetime|None=None
class PostResponse(BaseModel):
    title:str
    content:str
    id:int
    created_at:datetime
    owner_id:int
    owner: UserResponse # it will send data a/c to UserResponse schemas i.e., structure
    model_config=ConfigDict(from_attributes=True)

class AccessToken(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:Optional[str]|None=None

class VoteCreate(BaseModel):
    post_id:int
    dir:int

class VoteResponse(BaseModel):
    Post:PostResponse
    votes:int
    