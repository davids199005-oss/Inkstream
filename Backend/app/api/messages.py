from collections.abc import AsyncIterable

from fastapi import APIRouter
from fastapi.sse import EventSourceResponse, ServerSentEvent
from app.api.conversations import ConversationId
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
async def send_message(
    conversation_id: ConversationId,
    payload: MessageCreate,
) -> AsyncIterable[ServerSentEvent]:
    await conversation_service.get_conversation(conversation_id=conversation_id)
    async for event in message_service.add_message_stream(
        conversation_id=conversation_id,
        content=payload.content,
    ):
        yield event
