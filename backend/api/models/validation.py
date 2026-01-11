"""
Validation utilities that match the CLI app validation logic exactly.
"""
from typing import Union
from datetime import datetime


def validate_task_title(title: str) -> str:
    """
    Validate task title following the same rules as the CLI app.

    Args:
        title: The task title to validate

    Returns:
        The validated title

    Raises:
        ValueError: If the title doesn't meet validation criteria
    """
    if not title or not isinstance(title, str):
        raise ValueError("Task title must be a non-empty string")
    if len(title) > 100:
        raise ValueError("Task title must not exceed 100 characters")
    return title.strip()


def validate_task_description(description: str) -> str:
    """
    Validate task description following the same rules as the CLI app.

    Args:
        description: The task description to validate

    Returns:
        The validated description

    Raises:
        ValueError: If the description doesn't meet validation criteria
    """
    if description and len(description) > 500:
        raise ValueError("Task description must not exceed 500 characters")
    return description if description else ""


def validate_task_completed(completed: Union[bool, str]) -> bool:
    """
    Validate task completion status following the same rules as the CLI app.

    Args:
        completed: The completion status to validate

    Returns:
        The validated completion status

    Raises:
        ValueError: If the completion status is not a boolean
    """
    if not isinstance(completed, bool):
        # Try to convert string representations to boolean
        if isinstance(completed, str):
            if completed.lower() in ['true', '1', 'yes', 'on']:
                return True
            elif completed.lower() in ['false', '0', 'no', 'off']:
                return False
        raise ValueError("Task completed status must be a boolean")
    return completed


def validate_task_user_id(user_id: str) -> str:
    """
    Validate task user ID following the same rules as the CLI app.

    Args:
        user_id: The user ID to validate

    Returns:
        The validated user ID

    Raises:
        ValueError: If the user ID doesn't meet validation criteria
    """
    if not user_id or not isinstance(user_id, str):
        raise ValueError("Task user_id must be a non-empty string")
    return user_id.strip()