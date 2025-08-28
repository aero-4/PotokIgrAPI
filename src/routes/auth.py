from datetime import timedelta

from fastapi import APIRouter, HTTPException, status, Depends
from starlette.responses import RedirectResponse, JSONResponse

from src.depens.user import get_user_schema, check_refresh_payload, check_access_payload, get_user_reg_schema
from src.models.models import Game, GameScreens
from src.schemas.schemas import GameSchema, Paginate, LoginSchema, RegisterSchema, TokenInfo, Roles
from src.models.models import User
from src.utils.utils import get_hash_string, encode_jwt, random_string

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/login", response_model=TokenInfo)
async def login_handler(user=Depends(get_user_schema)):
    access_token = encode_jwt({'sub': user.username, 'type': 'access'}, expire_minutes=15)
    refresh_token = encode_jwt({'sub': user.username, 'type': 'refresh'}, expire_timedelta=timedelta(days=90))
    user.refresh = refresh_token
    await user.save()
    return TokenInfo(access_token=access_token, refresh_token=refresh_token, token_type="Bearer")


@auth_router.post("/token/refresh", response_model=TokenInfo)
async def refresh_handler(user=Depends(check_refresh_payload)):
    access_token = encode_jwt({'sub': user.username, 'type': 'access'}, expire_minutes=15)
    response = JSONResponse(status_code=200, content={})
    response.set_cookie("access_token", access_token, samesite="lax", secure=True, max_age=15 * 60)
    return response


@auth_router.post("/logout")
async def refresh_handler(user=Depends(check_refresh_payload)):
    user.refresh = None
    await user.save()
    return RedirectResponse("/")


@auth_router.post("/signup", response_model=TokenInfo)
async def signup_handler(user=Depends(get_user_reg_schema)):
    return await login_handler(user)
