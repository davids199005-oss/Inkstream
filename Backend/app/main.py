import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api import api_router
from app.core.database import close_database_connection, connect_to_database
from app.core.exceptions import ConversationNotFoundError


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    await connect_to_database()
    yield
    await close_database_connection()


app: FastAPI = FastAPI(
    title="Inkstream",
    description="Inkstream is a AI-powered chat platform.",
    lifespan=lifespan,
)


@app.exception_handler(exc_class_or_status_code=ConversationNotFoundError)
async def handle_conversation_not_found(
    _request: Request,
    exc: ConversationNotFoundError,
) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)},
    )


app.include_router(router=api_router)


@app.get(path="/")
async def root() -> dict[str, str]:
    return {"message": "Inkstream is a AI-powered chat platform Live now."}