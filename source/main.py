from fastapi import FastAPI
from routes.base import base_router
from routes.data import data_router
from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager
from helper.config import get_settings

@asynccontextmanager
async def start_db_client(app: FastAPI):
    settings = get_settings()
    app.mongodb_client = AsyncIOMotorClient(settings.MONGODB_URI)
    app.database = app.mongodb_client[settings.DATABASE_NAME]
    yield

    app.mongodb_client.close()


app = FastAPI(lifespan=start_db_client)
app.include_router(base_router)
app.include_router(data_router)