from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from fastapi.security import HTTPAuthorizationCredentials
from fastapi import Depends
from api.models.task import (
    TaskCreate, TaskUpdate, TaskToggle,
    TaskResponse, TaskListResponse,
    TaskSingleResponse
)
from api.models.error import ErrorResponse
from api.services.task_adapter import TaskAdapter
from ..utils.jwt_validator import get_current_user_id as get_current_user_id_from_token, verify_user_owns_resource
from fastapi.security import HTTPBearer

security = HTTPBearer()


async def get_current_user_id_from_token_dep(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Dependency to get current user ID from JWT token.
    Verifies the token and returns the user ID.
    """
    token = credentials.credentials
    try:
        user_id = get_current_user_id_from_token(token)
        return user_id
    except HTTPException:
        raise


router = APIRouter()


@router.get("/{user_id}/tasks", response_model=TaskListResponse)
async def get_tasks(user_id: str, current_user_id: str = Depends(get_current_user_id_from_token_dep)):
    """
    Get all tasks for a specific user.

    Args:
        user_id: The ID of the user whose tasks to retrieve
        current_user_id: The ID of the authenticated user (from token)

    Returns:
        List of all tasks for the user
    """
    # Verify that the authenticated user is requesting their own tasks
    verify_user_owns_resource(current_user_id, user_id)

    adapter = TaskAdapter(user_id=user_id)
    tasks = adapter.get_all_tasks()

    return TaskListResponse(tasks=tasks)


@router.get("/{user_id}/tasks/{id}", response_model=TaskSingleResponse)
async def get_task(user_id: str, id: int, current_user_id: str = Depends(get_current_user_id_from_token_dep)):
    """
    Get details of a specific task.

    Args:
        user_id: The ID of the user who owns the task
        id: The ID of the task to retrieve
        current_user_id: The ID of the authenticated user (from token)

    Returns:
        The requested task

    Raises:
        HTTPException: 404 if task not found
    """
    # Verify that the authenticated user is requesting their own task
    verify_user_owns_resource(current_user_id, user_id)

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
    task_create: TaskCreate,
    current_user_id: str = Depends(get_current_user_id_from_token_dep)
):
    """
    Create a new task for the user.

    Args:
        user_id: The ID of the user creating the task
        task_create: Task data to create
        current_user_id: The ID of the authenticated user (from token)

    Returns:
        The created task
    """
    # Verify that the authenticated user is creating tasks for themselves
    verify_user_owns_resource(current_user_id, user_id)

    adapter = TaskAdapter(user_id=user_id)
    task = adapter.create_task(task_create)

    return TaskSingleResponse(task=task)


@router.put("/{user_id}/tasks/{id}", response_model=TaskSingleResponse)
async def update_task(
    user_id: str,
    id: int,
    task_update: TaskUpdate,
    current_user_id: str = Depends(get_current_user_id_from_token_dep)
):
    """
    Update an existing task.

    Args:
        user_id: The ID of the user who owns the task
        id: The ID of the task to update
        task_update: Task data to update
        current_user_id: The ID of the authenticated user (from token)

    Returns:
        The updated task

    Raises:
        HTTPException: 400 if validation error, 404 if task not found
    """
    # Verify that the authenticated user is updating their own task
    verify_user_owns_resource(current_user_id, user_id)

    adapter = TaskAdapter(user_id=user_id)
    task = adapter.update_task(id, task_update)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task not found with id: {id}"
        )

    return TaskSingleResponse(task=task)


@router.delete("/{user_id}/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(user_id: str, id: int, current_user_id: str = Depends(get_current_user_id_from_token_dep)):
    """
    Delete a task.

    Args:
        user_id: The ID of the user who owns the task
        id: The ID of the task to delete
        current_user_id: The ID of the authenticated user (from token)

    Raises:
        HTTPException: 404 if task not found
    """
    # Verify that the authenticated user is deleting their own task
    verify_user_owns_resource(current_user_id, user_id)

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
    task_toggle: TaskToggle,
    current_user_id: str = Depends(get_current_user_id_from_token_dep)
):
    """
    Toggle the completion status of a task.

    Args:
        user_id: The ID of the user who owns the task
        id: The ID of the task to update
        task_toggle: New completion status
        current_user_id: The ID of the authenticated user (from token)

    Returns:
        The updated task

    Raises:
        HTTPException: 400 if validation error, 404 if task not found
    """
    # Verify that the authenticated user is updating their own task
    verify_user_owns_resource(current_user_id, user_id)

    adapter = TaskAdapter(user_id=user_id)
    task = adapter.toggle_completion(id, task_toggle)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task not found with id: {id}"
        )

    return TaskSingleResponse(task=task)