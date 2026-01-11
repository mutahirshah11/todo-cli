from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Task:
    """
    Represents a single todo item with unique identifier, content, and completion status.
    """
    id: int
    title: str
    description: str = ""
    completed: bool = False
    user_id: str = ""
    created_at: datetime = None
    updated_at: datetime = None

    def __post_init__(self):
        """Validate the task after initialization."""
        if self.id <= 0:
            raise ValueError("Task ID must be a positive integer")
        if not self.title or not isinstance(self.title, str):
            raise ValueError("Task title must be a non-empty string")
        if len(self.title) > 100:
            raise ValueError("Task title must not exceed 100 characters")
        if self.description and len(self.description) > 500:
            raise ValueError("Task description must not exceed 500 characters")
        if not isinstance(self.completed, bool):
            raise ValueError("Task completed status must be a boolean")
        if not self.user_id or not isinstance(self.user_id, str):
            raise ValueError("Task user_id must be a non-empty string")

        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()