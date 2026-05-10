import logging
from logging import Logger
from typing import cast
from openai import AsyncOpenAI, OpenAIError
from openai.types.chat import ChatCompletionMessageParam
from openai.types.chat.chat_completion import ChatCompletion
from app.core.config import config
from app.core.exceptions import OpenAIConnectionError
from app.core.openai_client import get_openai_client
from app.models import Message
from app.repositories import ConversationRepository, MessageRepository


logger: Logger = logging.getLogger(name=__name__)


class MessageService:

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

        history: list[Message] = await self._message_repository.list_by_conversation(
            conversation_id=conversation_id
        )

        try:
            assistant_content: str = await self._generate_assistant_reply(history=history)
        except OpenAIError as e:
            logger.error(msg=f"OpenAI request failed: {e}")
            raise OpenAIConnectionError(reason="upstream LLM error") from e

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

    async def _generate_assistant_reply(self, history: list[Message]) -> str:
        client: AsyncOpenAI = get_openai_client()

        messages: list[ChatCompletionMessageParam] = [
            {"role": "system", "content": self.SYSTEM_PROMPT},
        ]
        for msg in history:
            messages.append(cast(ChatCompletionMessageParam, {"role": msg.role, "content": msg.content}))

        completion: ChatCompletion = await client.chat.completions.create(
            model=config.openai_model,
            messages=messages,
            temperature=self.TEMPERATURE,
            max_tokens=self.MAX_TOKENS,
        )

        content: str | None = completion.choices[0].message.content
        if content is None:
            raise OpenAIConnectionError(reason="empty response from LLM")
        return content