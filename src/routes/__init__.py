from .comments import comments_router
from .games import games_router
from .auth import auth_router
from .user import user_router

routers = [
    games_router, auth_router, user_router, comments_router
]