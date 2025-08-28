import datetime
import random
import string

import jwt
from googletrans import Translator
from jwt import ExpiredSignatureError, PyJWTError
from starlette import status, exceptions
from tortoise import Model
import hashlib

from src.schemas.schemas import AuthJWT


def encode_jwt(
        payload: dict, private_key: str = AuthJWT.private_key, algorithm: str = AuthJWT.algorithm, expire_minutes: int = AuthJWT.expire_token_minutes,
        expire_timedelta: datetime.timedelta | None = None
):
    now = datetime.datetime.now(datetime.UTC)
    expire = now + expire_timedelta if expire_timedelta else now + datetime.timedelta(minutes=expire_minutes)
    payload.update(
        exp=expire,
        iat=now
    )
    encoded = jwt.encode(
        payload, private_key, algorithm
    )
    return encoded


def decode_jwt(token: str, public_key: str = AuthJWT.public_key, algorithm: str = AuthJWT.algorithm):
    try:
        payload = jwt.decode(
            token,
            public_key,
            algorithms=[algorithm]
        )
        return payload
    except ExpiredSignatureError:
        raise exceptions.HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token expired",
        )
    except PyJWTError:
        raise exceptions.HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate token",
        )


async def translate_text(org_text: str) -> str:
    async with Translator() as translator:
        result = await translator.translate(org_text, dest="ru")
        return result.text


def get_hash_string(s: str):
    return hashlib.sha256(s.encode()).hexdigest()


def random_string(length: int = 32):
    return "".join(random.sample(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=length))
