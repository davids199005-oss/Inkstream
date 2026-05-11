from collections.abc import AsyncIterable

from fastapi import APIRouter, Request
from fastapi.sse import EventSourceResponse, ServerSentEvent
from app.api.conversations import ConversationId
from app.core.rate_limit import limiter
from app.models import MessageCreate
from app.services import conversation_service, message_service


router: APIRouter = APIRouter(
    prefix="/conversations/{conversation_id}/messages",
    tags=["messages"],
)


@router.post(
    path="",
    response_class=EventSourceResponse,
)
@limiter.limit(limit_value="10/minute")
async def send_message(
    request: Request,
    conversation_id: ConversationId,
    payload: MessageCreate,
) -> AsyncIterable[ServerSentEvent]:
    await conversation_service.get_conversation(conversation_id=conversation_id)
    async for event in message_service.add_message_stream(
        conversation_id=conversation_id,
        content=payload.content,
    ):
        yield event