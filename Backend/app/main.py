from logging import Logger


import logging
from collections.abc import Awaitable, Callable
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.api import api_router
from app.core.config import config
from app.core.database import close_database_connection, connect_to_database
from app.core.exceptions import ConversationNotFoundError, OpenAIConnectionError
from app.core.openai_client import close_openai_client, connect_openai_client
from app.core.rate_limit import limiter


logger: Logger = logging.getLogger(name=__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    await connect_to_database()
    await connect_openai_client()
    yield
    await close_openai_client()
    await close_database_connection()


app: FastAPI = FastAPI(
    title="Inkstream",
    description="Inkstream is a AI-powered chat platform.",
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_exception_handler(
    exc_class_or_status_code=RateLimitExceeded,
    handler=_rate_limit_exceeded_handler,
)


@app.middleware(middleware_type="http")
async def add_security_headers(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    response: Response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    return response


app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=config.cors_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Accept", "Authorization"],
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


@app.exception_handler(exc_class_or_status_code=OpenAIConnectionError)
async def handle_openai_connection_error(
    _request: Request,
    exc: OpenAIConnectionError,
) -> JSONResponse:
    logger.error(msg=f"OpenAI connection error: {exc}")
    return JSONResponse(
        status_code=503,
        content={"detail": "Upstream LLM service unavailable"},
    )


app.include_router(router=api_router)


@app.get(path="/")
async def root() -> dict[str, str]:
    return {"message": "Inkstream is a AI-powered chat platform Live now."}