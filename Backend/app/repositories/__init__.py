from app.repositories.conversation_repository import ConversationRepository
from app.repositories.message_repository import MessageRepository

message_repository: MessageRepository = MessageRepository()
conversation_repository: ConversationRepository = ConversationRepository(
    message_repository=message_repository,
)

__all__ = [
    "ConversationRepository",
    "MessageRepository",
    "conversation_repository",
    "message_repository",
]