from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


class UserBase(BaseModel):
    email: EmailStr


class PostResponse(PostBase):
    created_at: datetime
    owner_id: int
    id: int
    owner: UserBase


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    created_at: datetime
    id: int


class AccessTokenBase(BaseModel):
    access_token: str
    type: str


class TokenDataBase(BaseModel):
    id: Optional[int] = None
