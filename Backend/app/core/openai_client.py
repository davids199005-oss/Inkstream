from logging import Logger
import logging
from openai import AsyncOpenAI
from .config import config


logger: Logger = logging.getLogger(name=__name__)
client: AsyncOpenAI | None = None


async def connect_openai_client() -> None:
    global client
    client = AsyncOpenAI(
        api_key=config.openai_api_key,
        timeout=30.0,
    )
    logger.info(msg=f"OpenAI client initialized (model: {config.openai_model})")


async def close_openai_client() -> None:
    global client
    if client is not None:
        await client.close()
        logger.info(msg="OpenAI client closed")
    client = None


def get_openai_client() -> AsyncOpenAI:
    if client is None:
        raise RuntimeError("OpenAI client not initialized")
    return client