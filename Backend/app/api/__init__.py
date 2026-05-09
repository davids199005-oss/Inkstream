from fastapi import APIRouter
from app.api.conversations import router as conversations_router

api_router: APIRouter = APIRouter(prefix="/api")
api_router.include_router(router=conversations_router)

__all__ = ["api_router"]