from datetime import datetime
from typing import Literal, TypeAlias
from pydantic import BaseModel, Field

Role: TypeAlias = Literal["user", "assistant"]


class MessageCreate(BaseModel):
    content: str = Field(min_length=1, max_length=10000)


class Message(BaseModel):
    id: str
    conversation_id: str
    role: Role
    content: str
    created_at: datetime


class MessagePair(BaseModel):
    user_message: Message
    assistant_message: Message
