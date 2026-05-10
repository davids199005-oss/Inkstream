class InkstreamError(Exception):
    """Base class for resource not found errors."""


class ConversationNotFoundError(InkstreamError):
    """Raised when a conversation is not found."""

    def __init__(self, conversation_id: str) -> None:
        self.conversation_id: str = conversation_id
        super().__init__(f"Conversation with id {conversation_id} not found.")
