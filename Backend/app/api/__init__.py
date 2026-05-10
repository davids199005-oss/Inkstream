from fastapi import APIRouter
from app.api.conversations import router as conversations_router
from app.api.messages import router as messages_router

api_router: APIRouter = APIRouter(prefix="/api")
api_router.include_router(router=conversations_router)
api_router.include_router(router=messages_router)

__all__ = ["api_router"]
