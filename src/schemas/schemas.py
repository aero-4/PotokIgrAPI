import datetime
from pathlib import Path
from typing import Optional
from pydantic import BaseModel


class Paginate(BaseModel):
    offset: int
    limit: int
    cat: Optional[str] = None
    search: Optional[str] = None


class GameSchema(BaseModel):
    title: str
    slug: str
    description: Optional[str]
    genre: str
    platform: str
    metacritic: int
    release_date: datetime.date
    background_image: str


class LoginSchema(BaseModel):
    username: str
    password: str
    captcha: Optional[str]


class RegisterSchema(BaseModel):
    username: str
    password: str
    email: str
    captcha: Optional[str]


class TokenInfo(BaseModel):
    refresh_token: Optional[str]
    access_token: str
    token_type: str


class UserGetMeSchema(BaseModel):
    user: str
    email: str


class CommentSchema(BaseModel):
    user: str
    game_id: int
    text: str
    date: str


class LikeSchema(BaseModel):
    id: int
    value: int


class AuthJWT:
    public_key: str = Path("src/certs/public.pem").read_text()
    private_key: str = Path("src/certs/private.pem").read_text()
    algorithm = "RS256"
    expire_token_minutes: int = 60


class Roles:
    ADMIN = 1
    USER = 0


class Vote:
    LIKE = 1
    DISLIKE = 0
