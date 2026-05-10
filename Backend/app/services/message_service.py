from app.models import Message
from app.repositories import ConversationRepository, MessageRepository


class MessageService:

    ECHO_PREFIX: str = "Echo (Phase 1 placeholder): "

    SYSTEM_PROMPT: str = (
        "You are Inky, a helpful AI assistant."
        " Be friendly and engaging in your responses."
        " Use markdown formatting when appropriate."
    )
    TEMPERATURE: float = 0.7
    MAX_TOKENS: int = 1000

    def __init__(
        self,
        message_repository: MessageRepository,
        conversation_repository: ConversationRepository,
    ) -> None:
        self._message_repository: MessageRepository = message_repository
        self._conversation_repository: ConversationRepository = conversation_repository

    async def add_message(
        self,
        conversation_id: str,
        content: str,
    ) -> tuple[Message, Message]:

        user_message: Message = await self._message_repository.create(
            conversation_id=conversation_id,
            role="user",
            content=content,
        )

        assistant_content: str = self._generate_assistant_reply(
            user_content=content
        )
        assistant_message: Message = await self._message_repository.create(
            conversation_id=conversation_id,
            role="assistant",
            content=assistant_content,
        )

        await self._conversation_repository.touch_updated(
            conversation_id=conversation_id
        )

        return user_message, assistant_message

    async def list_messages(self, conversation_id: str) -> list[Message]:
        return await self._message_repository.list_by_conversation(
            conversation_id=conversation_id
        )

    def _generate_assistant_reply(self, user_content: str) -> str:
        return f"{self.ECHO_PREFIX}{user_content}"
