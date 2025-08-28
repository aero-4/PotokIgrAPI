import random

from fastapi import APIRouter, HTTPException, status

from src.models.models import Game, GameScreens, Torrent
from src.schemas.schemas import GameSchema, Paginate

games_router = APIRouter(prefix="/games", tags=["Games"])


@games_router.post("/last")
async def last_games_handler(pag: Paginate):
    games = await Game.all().offset(pag.offset).limit(pag.limit)
    return games


@games_router.post("/cat")
async def games_by_cat(pag: Paginate):
    if pag.cat.lower() == "new":
        return await Game.all().order_by('-release_date').offset(pag.offset).limit(pag.limit)
    return await Game.filter(genre=pag.cat.title()).order_by('release_date').offset(pag.offset).limit(pag.limit)


@games_router.post("/search")
async def games_search(pag: Paginate):
    return await Game.filter(title__icontains=pag.search).offset(pag.offset).limit(pag.limit)


@games_router.get("/game/{slug}")
async def game_for_id(slug: str):
    game_data = await Game.filter(slug=slug).first().values()
    similar = await Game.filter(title__icontains=game_data["title"])
    similar_genres_games = await Game.filter(genre=game_data["genre"], torrent__isnull=False)
    random.shuffle(similar_genres_games)
    photo_urls = await GameScreens.filter(game_id=game_data["id"]).values_list("short_screenshot", flat=True)
    game_data["screens"] = list(set(photo_urls))
    game_data["torrent"] = [
        i for i in await Torrent.filter(game_id=game_data["id"]).order_by('seeders', '-id')
    ]
    game_data["similar_games"] = random.sample(similar_genres_games + similar, k=20)
    return game_data


@games_router.post("/new")
async def new_handler(schema: GameSchema):
    if await Game.get_or_none(title=schema.title):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This game already exist")

    await Game.create(
        title=schema.title,
        slug=schema.slug,
        description=schema.description,
        genre=schema.genre,
        platform=schema.platform,
        metacritic=schema.metacritic,
        release_date=schema.release_date,
        background_image=schema.background_image
    )
    return True
