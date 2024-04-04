from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional
from enum import Enum

class ItemBase(BaseModel):
    username: str | EmailStr
    password: str 
    website: str | HttpUrl
    notes: str


class ItemUpdate(BaseModel):
    username: Optional[str | EmailStr] = None
    password: Optional[str] = None 
    website: Optional[str | HttpUrl] =None
    notes: Optional[str] = None
    
    
class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id:int
    user_id: int

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    username: EmailStr


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    password: Optional[str] = None
    

class User(UserBase):
    id:int
    items: list[Item] = []
        
    class Config:
            from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    scopes: list[str]= []

class Tags(Enum):
    auth= 'authentication'
    user = 'user'
    items = 'items'