from typing import Annotated, TypeAlias
from fastapi import APIRouter, Path, Request, status
from app.core.rate_limit import limiter
from app.models import (
    Conversation,
    ConversationCreate,
    ConversationDetail,
    ConversationSummary,
    Message,
)
from app.services import conversation_service, message_service


ConversationId: TypeAlias = Annotated[
    str,
    Path(
        pattern=r"^[0-9a-fA-F]{24}$",
        description="MongoDB ObjectId (24-character hex string)",
    ),
]

router: APIRouter = APIRouter(prefix="/conversations", tags=["conversations"])


@router.get(path="", response_model=list[ConversationSummary])
@limiter.limit(limit_value="60/minute")
async def list_conversations(request: Request) -> list[ConversationSummary]:
    conversations: list[Conversation] = await conversation_service.list_conversations()
    return [
        ConversationSummary.model_validate(obj=conv.model_dump())
        for conv in conversations
    ]


@router.post(
    path="",
    response_model=ConversationSummary,
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit(limit_value="30/minute")
async def create_conversation(
    request: Request,
    payload: ConversationCreate,
) -> ConversationSummary:
    conversation: Conversation = await conversation_service.create_conversation(
        title=payload.title,
    )
    return ConversationSummary.model_validate(obj=conversation.model_dump())


@router.get(path="/{conversation_id}", response_model=ConversationDetail)
@limiter.limit(limit_value="60/minute")
async def get_conversation(
    request: Request,
    conversation_id: ConversationId,
) -> ConversationDetail:
    conversation: Conversation = await conversation_service.get_conversation(
        conversation_id=conversation_id,
    )
    messages: list[Message] = await message_service.list_messages(conversation_id=conversation_id)
    return ConversationDetail(
        id=conversation.id,
        title=conversation.title,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at,
        messages=messages,
    )


@router.delete(path="/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit(limit_value="20/minute")
async def delete_conversation(
    request: Request,
    conversation_id: ConversationId,
) -> None:
    await conversation_service.get_conversation(conversation_id=conversation_id)
    await conversation_service.delete_conversation(conversation_id=conversation_id)
