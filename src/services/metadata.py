import asyncio
import logging
import pprint
import httpx
import loguru
from httpx import QueryParams
from tortoise import Tortoise

from config import API_KEY_RAWGIO
from src.models.models import Game, GameScreens
from src.utils.utils import translate_text

logging.basicConfig(level=logging.INFO)


class MetadataParser:
    def __init__(self):
        self.API_URL = "https://api.rawg.io/api/games"

    async def run(self):
        await self.parser()

    async def parser(self):
        page = 1

        while True:
            try:
                results_data = await self.search_games(page)

                if len(results_data) == 0:
                    logging.info(f"Page: {page} FINISH!")
                    return

                for game_res in results_data:
                    _game = await Game.get_or_none(
                        title=game_res["name"],
                        slug=game_res["slug"],
                    )
                    if not _game and len(game_res["platform"]) > 0 and game_res["platforms"][0]["platform"]["name"].lower() == "pc":
                        _game = await Game.create(
                            title=game_res["name"],
                            slug=game_res["slug"],
                            genre=game_res["genres"][0]["name"] if len(game_res["genres"]) > 0 else "-",
                            platform=game_res["platforms"][0]["platform"]["name"],
                            metacritic=game_res.get("metacritic", 0),
                            release_date=game_res["released"],
                            background_image=game_res["background_image"],
                        )
                        logging.info(f"Added game - {game_res["name"]}")

                        if len(game_res["short_screenshots"]) > 0:
                            for shr_screen in game_res["short_screenshots"]:
                                await GameScreens.create(game_id=_game.id, short_screenshot=shr_screen["image"])
            except Exception as e:
                logging.error(f"Error load metadata: {e}")
            await asyncio.sleep(1)
            page += 1

    async def update_desc(self):
        try:
            games = await Game.filter(description__isnull=True).all()
            logging.info(f"Length: {len(games)}")
            for game in games:
                try:
                    data = await self.get_details_game(game.slug)
                    desc = await translate_text(data["description_raw"])
                    game.description = desc
                    await game.save()
                    logging.info(f"Set NEW desc - {desc}")
                except Exception as e:
                    logging.warning(f"Not translate this desc - {game}. Reason {e}")
        except Exception as e:
            logging.error("Not work update desc")

    async def search_games(self, page: int = 1):
        params = {
            "key": API_KEY_RAWGIO,
            "platforms": "1",
            "page_size": 80,
            "page": page,
        }
        return await self._get(params)

    async def get_details_game(self, slug: str):
        params = {
            "key": API_KEY_RAWGIO,
        }
        url = self.API_URL + f"/{slug}"
        return await self._get(params, url)

    async def _get(self, params: dict, url: str = None):
        async with httpx.AsyncClient(timeout=10) as client:
            try:
                r = await client.get(url or self.API_URL, params=QueryParams(params))
                r.raise_for_status()
                return r.json().get("results", []) if not url else r.json()
            except Exception as e:
                logging.error(f"Fail request {params}: {e}")
                return []


if __name__ == '__main__':
    asyncio.run(MetadataParser().run())
