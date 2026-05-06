from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field

Role = Literal["user", "assistant"]

class MessageCreate(BaseModel):
    content: str = Field(min_length=1, max_length=10000)


class Message(BaseModel):
    id: str 
    conversation_id: str
    role: Role
    content: str
    created_at: datetime
