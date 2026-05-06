from datetime import datetime
from pydantic import BaseModel, Field

class ConversationCreate(BaseModel):
    title: str = Field(default="New Conversation", max_length=200)


class Conversation(BaseModel):
    id: str 
    title: str
    created_at: datetime
    updated_at: datetime