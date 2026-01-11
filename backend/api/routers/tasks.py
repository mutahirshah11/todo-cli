from fastapi import APIRouter, HTTPException, status
from typing import List
from backend.api.models.task import (
    TaskCreate, TaskUpdate, TaskToggle,
    TaskResponse, TaskListResponse,
    TaskSingleResponse
)
from backend.api.models.error import ErrorResponse
from backend.api.services.task_adapter import TaskAdapter


router = APIRouter()


@router.get("/{user_id}/tasks", response_model=TaskListResponse)
async def get_tasks(user_id: str):
    """
    Get all tasks for a specific user.

    Args:
        user_id: The ID of the user whose tasks to retrieve

    Returns:
        List of all tasks for the user
    """
    adapter = TaskAdapter(user_id=user_id)
    tasks = adapter.get_all_tasks()

    return TaskListResponse(tasks=tasks)


@router.get("/{user_id}/tasks/{id}", response_model=TaskSingleResponse)
async def get_task(user_id: str, id: int):
    """
    Get details of a specific task.

    Args:
        user_id: The ID of the user who owns the task
        id: The ID of the task to retrieve

    Returns:
        The requested task

    Raises:
        HTTPException: 404 if task not found
    """
    adapter = TaskAdapter(user_id=user_id)
    task = adapter.get_task_by_id(id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task not found with id: {id}"
        )

    return TaskSingleResponse(task=task)


@router.post("/{user_id}/tasks", response_model=TaskSingleResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    user_id: str,
    task_create: TaskCreate
):
    """
    Create a new task for the user.

    Args:
        user_id: The ID of the user creating the task
        task_create: Task data to create

    Returns:
        The created task
    """
    adapter = TaskAdapter(user_id=user_id)
    task = adapter.create_task(task_create)

    return TaskSingleResponse(task=task)


@router.put("/{user_id}/tasks/{id}", response_model=TaskSingleResponse)
async def update_task(
    user_id: str,
    id: int,
    task_update: TaskUpdate
):
    """
    Update an existing task.

    Args:
        user_id: The ID of the user who owns the task
        id: The ID of the task to update
        task_update: Task data to update

    Returns:
        The updated task

    Raises:
        HTTPException: 400 if validation error, 404 if task not found
    """
    adapter = TaskAdapter(user_id=user_id)
    task = adapter.update_task(id, task_update)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task not found with id: {id}"
        )

    return TaskSingleResponse(task=task)


@router.delete("/{user_id}/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(user_id: str, id: int):
    """
    Delete a task.

    Args:
        user_id: The ID of the user who owns the task
        id: The ID of the task to delete

    Raises:
        HTTPException: 404 if task not found
    """
    adapter = TaskAdapter(user_id=user_id)
    success = adapter.delete_task(id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task not found with id: {id}"
        )


@router.patch("/{user_id}/tasks/{id}/complete", response_model=TaskSingleResponse)
async def toggle_task_completion(
    user_id: str,
    id: int,
    task_toggle: TaskToggle
):
    """
    Toggle the completion status of a task.

    Args:
        user_id: The ID of the user who owns the task
        id: The ID of the task to update
        task_toggle: New completion status

    Returns:
        The updated task

    Raises:
        HTTPException: 400 if validation error, 404 if task not found
    """
    adapter = TaskAdapter(user_id=user_id)
    task = adapter.toggle_completion(id, task_toggle)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task not found with id: {id}"
        )

    return TaskSingleResponse(task=task)