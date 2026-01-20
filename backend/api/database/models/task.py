from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime, timezone
from sqlmodel import Field, SQLModel
from enum import Enum
from sqlalchemy import Index

class TaskStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"

class Task(SQLModel, table=True):
    __tablename__ = "tasks"
    __table_args__ = (
        Index("idx_tasks_user_status", "user_id", "status"),
        Index("idx_tasks_user_deleted", "user_id", "deleted_at"),
    )

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: str = Field(foreign_key="users.user_id", index=True, nullable=False)
    title: str = Field(min_length=1)
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    deleted_at: Optional[datetime] = Field(default=None)
