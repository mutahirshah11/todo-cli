from dataclasses import dataclass
from typing import Optional


@dataclass
class Task:
    """
    Represents a single todo item with unique identifier, content, and completion status.
    """
    id: int
    content: str
    completed: bool = False

    def __post_init__(self):
        """Validate the task after initialization."""
        if self.id <= 0:
            raise ValueError("Task ID must be a positive integer")
        if not self.content or not isinstance(self.content, str):
            raise ValueError("Task content must be a non-empty string")
        if not isinstance(self.completed, bool):
            raise ValueError("Task completed status must be a boolean")