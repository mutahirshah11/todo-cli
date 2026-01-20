from uuid import UUID, uuid4
from datetime import datetime, timezone
from enum import Enum
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional

class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    conversation_id: UUID = Field(foreign_key="conversations.id", index=True, nullable=False)
    role: MessageRole = Field(nullable=False)
    content: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    conversation: Optional["Conversation"] = Relationship(back_populates="messages")
