"""
Request and Response schemas for the Todo API.
These schemas define the exact input/output format for all API endpoints.
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


# Reusing the task models from task.py since they are already defined there
from .task import TaskCreate, TaskUpdate, TaskToggle, TaskResponse


# Response models
class TaskListResponse(BaseModel):
    """Response model for listing tasks."""
    tasks: List[TaskResponse]


class TaskSingleResponse(BaseModel):
    """Response model for a single task."""
    task: TaskResponse


# Additional request/response schemas can be added here as needed