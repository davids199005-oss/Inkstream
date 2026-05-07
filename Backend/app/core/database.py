from pymongo.asynchronous.mongo_client import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase
from logging import Logger
import logging
from .config import config


logger: Logger = logging.getLogger(name=__name__)
client: AsyncMongoClient[dict[str, object]] | None = None
database: AsyncDatabase[dict[str, object]] | None = None

async def connect_to_database() -> None:
    global client, database
    client = AsyncMongoClient[dict[str, object]](config.mongo_uri)

    database = client.get_database(name=config.mongo_db_name)

    _ = await client.admin.command("ping")
    logger.info("Connected to MongoDB: %s", config.mongo_db_name)

async def close_database_connection() -> None:
    global client, database
    if client is not None:
        await client.close()
        logger.info("Disconnected from MongoDB")
    client = None
    database = None


def get_database() -> AsyncDatabase[dict[str, object]]:
    if database is None:
        raise RuntimeError("Database not connected")
    return database
