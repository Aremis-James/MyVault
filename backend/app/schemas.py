from pydantic import BaseModel, EmailStr, HttpUrl
from enum import Enum

class ItemBase(BaseModel):
    username: str | EmailStr
    password: str 
    website: str | HttpUrl
    notes: str

    
class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id:int
    user_id: int

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str
    

class User(UserBase):
    id:int
    items: list[Item] = []
        
    class Config:
            from_attributes = True


class Tags(Enum):
     item = 'items'
     users = 'users'
     