from uuid import UUID, uuid4
from datetime import datetime, timezone
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship

class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: str = Field(foreign_key="users.user_id", index=True, nullable=False)
    title: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    messages: List["Message"] = Relationship(back_populates="conversation")
