import datetime
from typing import List

from cachetools import TTLCache
from fastapi import APIRouter, Depends, Body, HTTPException, status

from src.models.models import TorrentComment, TorrentCommentLikes, User
from src.depens.user import validate_auth_user
from src.schemas.schemas import CommentSchema, LikeSchema

ttl_cache = TTLCache(ttl=60, maxsize=100000)
comments_router = APIRouter(prefix="/comments", tags=["Comments"])


@comments_router.post("/last")
async def last_comments(body=Body(...)):
    comments = await TorrentComment.filter(game_id=int(body.get("game_id"))).order_by('-id')
    return comments


@comments_router.post("/new")
async def new_comment(comm: CommentSchema = Body(...), user=Depends(validate_auth_user)):
    if ttl_cache.get(user.username) == comm.text:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Same text comment")

    _comm = await TorrentComment.create(
        user=user.username, game_id=comm.game_id, text=comm.text, date=comm.date
    )
    ttl_cache[user.username] = comm.text
    return {"msg": "ok", "comm": _comm}


@comments_router.get("/likes/{id}")
async def my_likes_comment(id: int, user: User = Depends(validate_auth_user)):
    return await TorrentCommentLikes.filter(user_id=user.id)


@comments_router.post("/like")
async def like_comment(comm: LikeSchema = Body(...), user: User = Depends(validate_auth_user)):
    if await TorrentCommentLikes.get_or_none(comment_id=comm.id):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You vote this comment")

    last_comm = await TorrentComment.get_or_none(id=comm.id)
    last_comm.value = comm.value
    await last_comm.save()

    await TorrentCommentLikes.create(
        comment=last_comm,
        user_id=user.id,
        value=comm.value
    )
    return {"msg": "ok"}
