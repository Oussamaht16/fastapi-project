from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint


# hadi bch nthkmo fl output ta3 user
class User(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


# hadi hia pydantic class li drnaha bch nthakmo fl output mais khassat haja bch ymchi class config


class Post(BaseModel):
    # hadi rani aplikitha post o l get all post mais fi get all post lazam nzido list psQ rahom bzf o hia valid lwhda
    id: int
    title: str
    content: str
    owner_id: int
    owner: User
    # published: bool
    # id: int
    # created_at: datetime

    class Config:
        # هذا تحذير من مكتبة Pydantic v2. يخبرك بأنّ orm_mode=True تم تغيير اسمه في النسخة الجديدة إلى from_attributes=True. إذا كنت تستخدم Pydantic BaseModel مع قواعد بيانات، فعليك تعديل الكود.
        # orm_mode = True
        from_attributes = True


# Hadi la class halitha bal3ani bch users ki ji ydakhl email wa password yktabhom b sigha jayida


class UserIn(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)  # 1 for upvote, 0 for downvote


# this schema for getting and avoing mistakes when we want to get the post with its votes number
class PostVote(BaseModel):
    Post: Post
    votes: int

    class Config:
        from_attributes = True
