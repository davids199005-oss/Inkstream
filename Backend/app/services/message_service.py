import logging
from collections.abc import AsyncIterator
from logging import Logger
from openai.types.chat.parsed_chat_completion import ParsedChatCompletion
from typing import cast
from fastapi.sse import ServerSentEvent
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

    TITLE_SYSTEM_PROMPT: str = (
        "You are a title generator for a chat application."
        " Given a conversation, generate a concise title in 3-5 words"
        " capturing the main topic.\n\n"
        "Rules:\n"
        "- 3-5 words maximum\n"
        "- Title Case\n"
        "- No quotes, no trailing punctuation\n"
        "- English only\n\n"
        "Example:\n"
        "Conversation:\n"
        "User: How do I filter a pandas DataFrame by multiple conditions?\n"
        "Assistant: You can use boolean indexing with & and | operators...\n\n"
        "Title: Pandas DataFrame Filtering Conditions\n\n"
        "Now generate a title for the following conversation:"
    )
    TITLE_TEMPERATURE: float = 0.3
    TITLE_MAX_TOKENS: int = 50

    def __init__(
        self,
        message_repository: MessageRepository,
        conversation_repository: ConversationRepository,
    ) -> None:
        self._message_repository: MessageRepository = message_repository
        self._conversation_repository: ConversationRepository = conversation_repository

    

    async def list_messages(self, conversation_id: str) -> list[Message]:
        return await self._message_repository.list_by_conversation(
            conversation_id=conversation_id
        )


    async def _generate_title(self, history: list[Message]) -> str:
        client: AsyncOpenAI = get_openai_client()
        conversation_text: str = "\n".join(
            f"{msg.role.capitalize()}: {msg.content}" for msg in history)

        messages: list[ChatCompletionMessageParam] = [
            {"role": "system", "content": self.TITLE_SYSTEM_PROMPT},
            {"role": "user", "content": conversation_text},
        ]

        completion: ChatCompletion = await client.chat.completions.create(
            model=config.openai_model,
            messages=messages,
            temperature=self.TITLE_TEMPERATURE,
            max_tokens=self.TITLE_MAX_TOKENS,
        )

        title: str | None = completion.choices[0].message.content
        if title is None:
            raise OpenAIConnectionError(reason="empty response from LLM")
        return title.strip()

    async def add_message_stream(
        self,
        conversation_id: str,
        content: str,
    ) -> AsyncIterator[ServerSentEvent]:
        user_message: Message = await self._message_repository.create(
            conversation_id=conversation_id,
            role="user",
            content=content,
        )

        yield ServerSentEvent(
            event="user_message_saved",
            data=user_message,
        )

        history: list[Message] = await self._message_repository.list_by_conversation(
            conversation_id=conversation_id
        )

        messages: list[ChatCompletionMessageParam] = [
            {"role": "system", "content": self.SYSTEM_PROMPT},
        ]
        for msg in history:
            messages.append(
                cast(
                    ChatCompletionMessageParam,
                    {"role": msg.role, "content": msg.content},
                )
            )

        
        try:
            client: AsyncOpenAI = get_openai_client()
            async with client.chat.completions.stream(
                model=config.openai_model,
                messages=messages,
                temperature=self.TEMPERATURE,
                max_tokens=self.MAX_TOKENS,
            ) as stream:
                async for event in stream:
                    if event.type == "content.delta":
                        yield ServerSentEvent(
                            event="token",
                            data={"text": event.delta},
                        )

                completion: ParsedChatCompletion[None] = await stream.get_final_completion()

            assistant_content: str | None = completion.choices[0].message.content
            if assistant_content is None:
                raise OpenAIConnectionError(reason="empty response from LLM")

            assistant_message: Message = await self._message_repository.create(
                conversation_id=conversation_id,
                role="assistant",
                content=assistant_content,
            )

            new_title: str | None = None
            if len(history) == 1:
                try:
                    new_title = await self._generate_title(
                        history=[*history, assistant_message]
                    )
                    await self._conversation_repository.update_title(
                        conversation_id=conversation_id,
                        title=new_title,
                    )
                except OpenAIError as title_error:
                    logger.error(msg=f"Title generation failed: {title_error}")
                    new_title = None

            if new_title is None:
                await self._conversation_repository.touch_updated(
                    conversation_id=conversation_id
                )

            yield ServerSentEvent(
                event="done",
                data={
                    "assistant_message_id": assistant_message.id,
                    "title": new_title,
                },
            )

        except (OpenAIError, OpenAIConnectionError) as stream_error:
            logger.error(msg=f"OpenAI streaming failed: {stream_error}")
            yield ServerSentEvent(
                event="error",
                data={"message": "Stream interrupted"},
            )
