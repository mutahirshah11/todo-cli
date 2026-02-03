import uuid
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum

if TYPE_CHECKING:
    from .task import Task  # Adjust import path as needed

class TaskStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"

class User(SQLModel, table=True):
    __tablename__ = "users"

    user_id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    name: str = Field(max_length=255)  # Store user's name
    email: str = Field(unique=True, index=True, max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)

    # Relationship to tasks
    tasks: List["Task"] = Relationship(back_populates="user")


class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    is_completed: bool = Field(default=False)
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    user_id: str = Field(foreign_key="users.user_id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    deleted_at: Optional[datetime] = Field(default=None)

    # Relationship to user
    user: Optional[User] = Relationship(back_populates="tasks")

    def __init__(self, **data):
        super().__init__(**data)
        # Sync status and is_completed on initialization
        if "status" in data and "is_completed" not in data:
            self.is_completed = (self.status == TaskStatus.COMPLETED)
        elif "is_completed" in data and "status" not in data:
            self.status = TaskStatus.COMPLETED if self.is_completed else TaskStatus.PENDING