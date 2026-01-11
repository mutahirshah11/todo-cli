from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime


class TaskBase(BaseModel):
    """Base model for task with common fields."""
    title: str = Field(..., min_length=1, max_length=100, description="Task title (1-100 characters)")
    description: Optional[str] = Field(default="", max_length=500, description="Task description (max 500 characters)")

    @field_validator('title')
    @classmethod
    def validate_title(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError("Task title must be a non-empty string")
        if len(v) > 100:
            raise ValueError("Task title must not exceed 100 characters")
        return v.strip()

    @field_validator('description')
    @classmethod
    def validate_description(cls, v):
        if v and len(v) > 500:
            raise ValueError("Task description must not exceed 500 characters")
        return v if v else ""


class TaskCreate(TaskBase):
    """Model for creating a new task."""
    completed: bool = False


class TaskUpdate(TaskBase):
    """Model for updating an existing task."""
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    completed: Optional[bool] = None

    @field_validator('title')
    @classmethod
    def validate_title_optional(cls, v):
        if v is not None:
            if not v or len(v.strip()) == 0:
                raise ValueError("Task title must be a non-empty string")
            if len(v) > 100:
                raise ValueError("Task title must not exceed 100 characters")
            return v.strip()
        return v


class TaskToggle(BaseModel):
    """Model for toggling task completion status."""
    completed: bool


class TaskResponse(TaskBase):
    """Response model for a task with all fields."""
    id: int
    completed: bool
    created_at: datetime
    updated_at: datetime
    user_id: str


class TaskListResponse(BaseModel):
    """Response model for listing tasks."""
    tasks: list[TaskResponse]


class TaskSingleResponse(BaseModel):
    """Response model for a single task."""
    task: TaskResponse