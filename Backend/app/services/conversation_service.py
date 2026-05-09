from app.models import Conversation
from app.repositories import ConversationRepository

class ConversationService:
    def __init__(self, conversation_repository: ConversationRepository) -> None:
        self._conversation_repository: ConversationRepository = conversation_repository
    
    async def create_conversation(self, title: str) -> Conversation:
        return await self._conversation_repository.create(title=title)
    
    async def list_conversations(self) -> list[Conversation]:
        return await self._conversation_repository.list_all()

    async def get_conversation(self, conversation_id: str) -> Conversation | None:
        return await self._conversation_repository.find_by_id(conversation_id=conversation_id)

    async def delete_conversation(self, conversation_id: str) -> bool:
        return await self._conversation_repository.delete(conversation_id=conversation_id)