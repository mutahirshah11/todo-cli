"""
Task Validation Module
Contains validation rules that match the console app behavior
"""

from typing import Optional
from pydantic import BaseModel, validator, ValidationError
from datetime import datetime
import re


class TaskValidationRules:
    """
    Contains validation rules that match the console app behavior.
    """

    # Console app validation constants
    MAX_TITLE_LENGTH = 100
    MAX_DESCRIPTION_LENGTH = 500
    MIN_TITLE_LENGTH = 1

    @classmethod
    def validate_title(cls, title: str) -> str:
        """
        Validate task title according to console app rules.

        Args:
            title: The title to validate

        Returns:
            Validated title

        Raises:
            ValueError: If title doesn't meet validation criteria
        """
        if not title or not isinstance(title, str):
            raise ValueError("Task title must be a non-empty string")

        title = title.strip()

        if len(title) < cls.MIN_TITLE_LENGTH:
            raise ValueError("Task title must be at least 1 character long")

        if len(title) > cls.MAX_TITLE_LENGTH:
            raise ValueError(f"Task title must not exceed {cls.MAX_TITLE_LENGTH} characters")

        return title

    @classmethod
    def validate_description(cls, description: Optional[str]) -> str:
        """
        Validate task description according to console app rules.

        Args:
            description: The description to validate

        Returns:
            Validated description

        Raises:
            ValueError: If description doesn't meet validation criteria
        """
        if description is None:
            description = ""

        if not isinstance(description, str):
            raise ValueError("Task description must be a string")

        if len(description) > cls.MAX_DESCRIPTION_LENGTH:
            raise ValueError(f"Task description must not exceed {cls.MAX_DESCRIPTION_LENGTH} characters")

        return description.strip()

    @classmethod
    def validate_completed(cls, completed: bool) -> bool:
        """
        Validate task completion status according to console app rules.

        Args:
            completed: The completion status to validate

        Returns:
            Validated completion status

        Raises:
            ValueError: If completion status is not a boolean
        """
        if not isinstance(completed, bool):
            raise ValueError("Task completed status must be a boolean")

        return completed

    @classmethod
    def validate_user_id(cls, user_id: str) -> str:
        """
        Validate user ID according to console app rules.

        Args:
            user_id: The user ID to validate

        Returns:
            Validated user ID

        Raises:
            ValueError: If user ID doesn't meet validation criteria
        """
        if not user_id or not isinstance(user_id, str):
            raise ValueError("Task user_id must be a non-empty string")

        user_id = user_id.strip()

        # Additional validation: user_id should be a valid UUID format or similar identifier
        # For now, just ensure it's not empty after stripping
        if not user_id:
            raise ValueError("Task user_id must be a non-empty string")

        return user_id

    @classmethod
    def validate_task_fields(cls, title: str, description: Optional[str] = None,
                           completed: bool = False, user_id: str = "") -> tuple:
        """
        Validate all task fields according to console app rules.

        Args:
            title: Task title
            description: Task description (optional)
            completed: Task completion status
            user_id: User ID

        Returns:
            Tuple of validated fields (title, description, completed, user_id)

        Raises:
            ValueError: If any field doesn't meet validation criteria
        """
        validated_title = cls.validate_title(title)
        validated_description = cls.validate_description(description)
        validated_completed = cls.validate_completed(completed)
        validated_user_id = cls.validate_user_id(user_id) if user_id else user_id

        return validated_title, validated_description, validated_completed, validated_user_id


def validate_task_creation(title: str, description: Optional[str] = None) -> tuple:
    """
    Validate task creation parameters according to console app rules.

    Args:
        title: Task title
        description: Task description (optional)

    Returns:
        Tuple of validated (title, description)

    Raises:
        ValueError: If validation fails
    """
    validated_title, validated_description, _, _ = TaskValidationRules.validate_task_fields(
        title, description
    )
    return validated_title, validated_description


def validate_task_update(title: str, description: str = "") -> tuple:
    """
    Validate task update parameters according to console app rules.

    Args:
        title: Task title
        description: Task description

    Returns:
        Tuple of validated (title, description)

    Raises:
        ValueError: If validation fails
    """
    validated_title, validated_description, _, _ = TaskValidationRules.validate_task_fields(
        title, description
    )
    return validated_title, validated_description


def validate_task_completion(completion_status: bool) -> bool:
    """
    Validate task completion status according to console app rules.

    Args:
        completion_status: Task completion status

    Returns:
        Validated completion status

    Raises:
        ValueError: If validation fails
    """
    return TaskValidationRules.validate_completed(completion_status)


# Pydantic models with validation that matches console app behavior
from api.models.task import TaskCreate, TaskUpdate, TaskToggle


def validate_task_create_model(task_create: TaskCreate) -> TaskCreate:
    """
    Validate a TaskCreate model according to console app rules.

    Args:
        task_create: TaskCreate model to validate

    Returns:
        Validated TaskCreate model

    Raises:
        ValueError: If validation fails
    """
    # Validate individual fields
    validated_title, validated_description, _, _ = TaskValidationRules.validate_task_fields(
        task_create.title, task_create.description
    )

    # Update the model with validated values
    task_create.title = validated_title
    task_create.description = validated_description

    return task_create


def validate_task_update_model(task_update: TaskUpdate) -> TaskUpdate:
    """
    Validate a TaskUpdate model according to console app rules.

    Args:
        task_update: TaskUpdate model to validate

    Returns:
        Validated TaskUpdate model

    Raises:
        ValueError: If validation fails
    """
    # Validate individual fields
    validated_title, validated_description, _, _ = TaskValidationRules.validate_task_fields(
        task_update.title, task_update.description
    )

    # Update the model with validated values
    task_update.title = validated_title
    task_update.description = validated_description

    return task_update


def validate_task_toggle_model(task_toggle: TaskToggle) -> TaskToggle:
    """
    Validate a TaskToggle model according to console app rules.

    Args:
        task_toggle: TaskToggle model to validate

    Returns:
        Validated TaskToggle model

    Raises:
        ValueError: If validation fails
    """
    # Validate completion status
    validated_completed = TaskValidationRules.validate_completed(task_toggle.completed)

    # Update the model with validated value
    task_toggle.completed = validated_completed

    return task_toggle