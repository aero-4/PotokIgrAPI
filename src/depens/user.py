import logging

import httpx
from fastapi import HTTPException, Depends, Body
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette import status
from starlette.requests import Request

from config import RECAPTCHA_SECRET
from src.models.models import User
from src.schemas.schemas import LoginSchema, RegisterSchema, Roles
from src.utils.utils import get_hash_string, decode_jwt

GOOGLE_VERIFY_URL = "https://www.google.com/recaptcha/api/siteverify"


async def verify_recaptcha(token: str, remote_ip: str = None) -> bool:
    data = {
        "secret": RECAPTCHA_SECRET,
        "response": token,
    }
    if remote_ip:
        data["remoteip"] = remote_ip

    async with httpx.AsyncClient() as client:
        resp = await client.post(GOOGLE_VERIFY_URL, data=data)
        result = resp.json()

    return result.get("success", False)


async def check_captcha_token(schema):
    check_captcha = await verify_recaptcha(schema.captcha)
    logging.info(check_captcha)

    if not check_captcha:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Fail captcha")


async def get_user_schema(schema: LoginSchema = Body(...)):
    await check_captcha_token(schema)

    user = await User.get_or_none(username=schema.username, password=get_hash_string(schema.password))

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong login or password")

    return user


async def get_user_reg_schema(schema: RegisterSchema = Body(...)):
    await check_captcha_token(schema)

    user = await User.get_or_none(username=schema.username)

    if user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User already exist")

    user = await User.create(
        username=schema.username,
        email=schema.email,
        password=get_hash_string(schema.password),
        role=Roles.USER
    )
    return user


def check_access_payload(request: Request):
    token = request.cookies.get('access_token')
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorization")
    payload = decode_jwt(token)
    if payload.get("type") != "access":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong token type")
    return payload


async def check_refresh_payload(request: Request):
    token = request.cookies.get('refresh_token')
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorization")
    payload = decode_jwt(token)
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong token type")

    username = payload.get("sub")
    if not (user := await User.get_or_none(username=username)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    if user.refresh != token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    return user


async def validate_auth_user(payload: dict = Depends(check_access_payload)):
    username = payload.get("sub")
    if not (user := await User.filter(username=username).first()):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user
