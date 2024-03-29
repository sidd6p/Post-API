from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint


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


class PostResponseBase(PostBase):
    created_at: datetime
    owner_id: int
    id: int
    owner: UserBase


class PostVoteResponse(PostResponseBase):
    post: PostResponseBase
    votes: int


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


class VoteBase(BaseModel):
    post_id: int
    add_vote: conint(le=1)  # type: ignore
