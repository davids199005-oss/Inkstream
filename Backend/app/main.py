

import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager
from .core.database import connect_to_database, close_database_connection



logging.basicConfig(
    level=logging.INFO,
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

@asynccontextmanager
async def lifespan(_app: FastAPI):
    await connect_to_database()
    yield
    await close_database_connection()

app: FastAPI = FastAPI(
    title="Inkstream",
    description="Inkstream is a ChatGPT style chat platform.",
)


@app.get(path="/")
async def root() -> dict[str, str]:
    return {"message": "Inkstream is a ChatGPT style chat platform Live now."}