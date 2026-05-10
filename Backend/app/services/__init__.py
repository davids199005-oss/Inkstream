from app.repositories import conversation_repository, message_repository
from app.services.conversation_service import ConversationService
from app.services.message_service import MessageService

conversation_service: ConversationService = ConversationService(
    conversation_repository=conversation_repository,
)
message_service: MessageService = MessageService(
    message_repository=message_repository,
    conversation_repository=conversation_repository,
)

__all__ = [
    "ConversationService",
    "MessageService",
    "conversation_service",
    "message_service",
]
