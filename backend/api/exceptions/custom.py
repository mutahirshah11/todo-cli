"""
Custom exception classes for the Todo API.
"""
from typing import Optional


class TaskNotFoundError(Exception):
    """Raised when a task is not found."""
    def __init__(self, task_id: int, message: Optional[str] = None):
        self.task_id = task_id
        self.message = message or f"Task not found with id: {task_id}"
        super().__init__(self.message)


class UserAccessError(Exception):
    """Raised when a user tries to access a resource they don't own."""
    def __init__(self, message: Optional[str] = None):
        self.message = message or "User does not have access to this resource"
        super().__init__(self.message)


class ValidationError(Exception):
    """Raised when validation fails."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class AuthenticationError(Exception):
    """Raised when authentication fails."""
    def __init__(self, message: Optional[str] = None):
        self.message = message or "Authentication failed"
        super().__init__(self.message)


class AuthorizationError(Exception):
    """Raised when authorization fails."""
    def __init__(self, message: Optional[str] = None):
        self.message = message or "Authorization failed"
        super().__init__(self.message)