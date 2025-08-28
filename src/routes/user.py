from datetime import timedelta

from fastapi import APIRouter, HTTPException, status, Depends
from starlette.responses import RedirectResponse, JSONResponse

from src.depens.user import get_user_schema, check_refresh_payload, check_access_payload, get_user_reg_schema, validate_auth_user
from src.models.models import Game, GameScreens
from src.schemas.schemas import GameSchema, Paginate, LoginSchema, RegisterSchema, TokenInfo, Roles, UserGetMeSchema
from src.models.models import User
from src.utils.utils import get_hash_string, encode_jwt, random_string

user_router = APIRouter(prefix="/user", tags=["User"])


@user_router.get("/me", response_model=UserGetMeSchema)
async def login_handler(user=Depends(validate_auth_user)):
    return UserGetMeSchema(user=user.username, email=user.email)
