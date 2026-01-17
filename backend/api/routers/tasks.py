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
from ..database.session import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession

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


@router.get("/tasks", response_model=TaskListResponse)
async def get_tasks(
    current_user_id: str = Depends(get_current_user_id_from_token_dep),
    session=Depends(get_db_session)
):
    """
    Get all tasks for the authenticated user.

    Args:
        current_user_id: The ID of the authenticated user (from token)

    Returns:
        List of all tasks for the user
    """
    adapter = TaskAdapter(session=session, user_id=current_user_id)
    tasks = await adapter.get_all_tasks()

    return TaskListResponse(tasks=tasks)


@router.get("/tasks/{id}", response_model=TaskSingleResponse)
async def get_task(
    id: str,
    current_user_id: str = Depends(get_current_user_id_from_token_dep),
    session: AsyncSession = Depends(get_db_session)
):
    """
    Get details of a specific task.

    Args:
        id: The ID of the task to retrieve
        current_user_id: The ID of the authenticated user (from token)

    Returns:
        The requested task

    Raises:
        HTTPException: 404 if task not found
    """

    adapter = TaskAdapter(session=session, user_id=current_user_id)
    task = await adapter.get_task_by_id(id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task not found with id: {id}"
        )

    return TaskSingleResponse(task=task)


@router.post("/tasks", response_model=TaskSingleResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_create: TaskCreate,
    current_user_id: str = Depends(get_current_user_id_from_token_dep),
    session: AsyncSession = Depends(get_db_session)
):
    """
    Create a new task for the authenticated user.

    Args:
        task_create: Task data to create
        current_user_id: The ID of the authenticated user (from token)

    Returns:
        The created task
    """

    adapter = TaskAdapter(session=session, user_id=current_user_id)
    task = await adapter.create_task(task_create)

    return TaskSingleResponse(task=task)


@router.put("/tasks/{id}", response_model=TaskSingleResponse)
async def update_task(
    id: str,
    task_update: TaskUpdate,
    current_user_id: str = Depends(get_current_user_id_from_token_dep),
    session: AsyncSession = Depends(get_db_session)
):
    """
    Update an existing task.

    Args:
        id: The ID of the task to update
        task_update: Task data to update
        current_user_id: The ID of the authenticated user (from token)

    Returns:
        The updated task

    Raises:
        HTTPException: 400 if validation error, 404 if task not found
    """

    adapter = TaskAdapter(session=session, user_id=current_user_id)
    task = await adapter.update_task(id, task_update)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task not found with id: {id}"
        )

    return TaskSingleResponse(task=task)


@router.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    id: str,
    current_user_id: str = Depends(get_current_user_id_from_token_dep),
    session: AsyncSession = Depends(get_db_session)
):
    """
    Delete a task.

    Args:
        id: The ID of the task to delete
        current_user_id: The ID of the authenticated user (from token)

    Raises:
        HTTPException: 404 if task not found
    """

    adapter = TaskAdapter(session=session, user_id=current_user_id)
    success = await adapter.delete_task(id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task not found with id: {id}"
        )


@router.patch("/tasks/{id}/complete", response_model=TaskSingleResponse)
async def toggle_task_completion(
    id: str,
    task_toggle: TaskToggle,
    current_user_id: str = Depends(get_current_user_id_from_token_dep),
    session: AsyncSession = Depends(get_db_session)
):
    """
    Toggle the completion status of a task.

    Args:
        id: The ID of the task to update
        task_toggle: New completion status
        current_user_id: The ID of the authenticated user (from token)

    Returns:
        The updated task

    Raises:
        HTTPException: 400 if validation error, 404 if task not found
    """

    adapter = TaskAdapter(session=session, user_id=current_user_id)
    task = await adapter.toggle_completion(id, task_toggle)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task not found with id: {id}"
        )

    return TaskSingleResponse(task=task)