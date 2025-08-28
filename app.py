import datetime
import random
import sys

import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise import Tortoise
from src.models.models import User
from src.routes import routers
from src.schemas.schemas import Roles
from src.services.metadata import MetadataParser
import src.services.torrent as torrent
from src.utils.utils import random_string, get_hash_string
# python -m uvicorn app:app --reload
scheduler = AsyncIOScheduler()

scheduler.add_job(MetadataParser().run, CronTrigger(hour=4), next_run_time=datetime.datetime.now())
scheduler.add_job(MetadataParser().update_desc, CronTrigger(hour=8), next_run_time=datetime.datetime.now())
scheduler.add_job(torrent.run, CronTrigger(hour=12), next_run_time=datetime.datetime.now())
scheduler.start()



async def add_admin():
    pasw = random_string()
    user = f"Admin{random.randint(1000, 99999)}"
    await User.create(
        username=user,
        email=f"{random_string()}@gmail.com",
        password=get_hash_string(pasw),
        role=Roles.ADMIN
    )
    print(user, pasw)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await Tortoise.init(config={
        "connections": {"default": "sqlite://db.sqlite3"},
        "apps": {
            "models": {
                "models": ['src.models.models'],
                "default_connection": "default",
            }
        },
    })
    print("Tortoise ORM initialized")
    await Tortoise.generate_schemas(safe=True)
    yield
    await Tortoise.close_connections()
    print("Tortoise ORM connections closed")


app = FastAPI(
    title="API PotokIgr",
    lifespan=lifespan,
    version="0.0.1",
)

origins = [
    "https://potok.cloud"
]

for r in routers:
    app.include_router(r)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
