from fastapi import APIRouter, status

from app.api.conversations import ConversationId
from app.models import Message, MessageCreate, MessagePair
from app.services import conversation_service, message_service


router: APIRouter = APIRouter(
    prefix="/conversations/{conversation_id}/messages",
    tags=["messages"],
)


@router.post(
    path="",
    response_model=MessagePair,
    status_code=status.HTTP_201_CREATED,
)
async def add_message(
    conversation_id: ConversationId,
    payload: MessageCreate,
) -> MessagePair:
    await conversation_service.get_conversation(conversation_id=conversation_id)
    user_message: Message
    assistant_message: Message
    user_message, assistant_message = await message_service.add_message(
        conversation_id=conversation_id,
        content=payload.content,
    )
    return MessagePair(
        user_message=user_message,
        assistant_message=assistant_message,
    )