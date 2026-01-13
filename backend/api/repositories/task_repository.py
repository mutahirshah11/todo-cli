from typing import List, Optional
from sqlmodel import select, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from ..models.database import Task, User
from ..database.session import DatabaseErrorHandler
from datetime import datetime


class TaskRepository:
    """
    Repository class for handling Task database operations.
    Implements CRUD operations for tasks with proper error handling and user ownership validation.
    """

    def __init__(self, session):
        """
        Initialize the TaskRepository with a database session.

        Args:
            session: Async database session from SQLModel
        """
        self.session = session
        self.error_handler = DatabaseErrorHandler()

    async def get_tasks_by_user(self, user_id: str) -> List[Task]:
        """
        Retrieve all tasks for a specific user.

        Args:
            user_id: The ID of the user whose tasks to retrieve

        Returns:
            List of Task objects belonging to the user
        """
        try:
            statement = select(Task).where(Task.user_id == user_id).order_by(Task.created_at.desc())
            result = await self.session.execute(statement)
            return result.scalars().all()
        except Exception as e:
            self.error_handler.handle_database_error(e, "Getting tasks by user")
            raise

    async def get_task_by_id(self, task_id: str, user_id: str) -> Optional[Task]:
        """
        Retrieve a specific task by its ID and user ID.

        Args:
            task_id: The ID of the task to retrieve
            user_id: The ID of the user who owns the task

        Returns:
            Task object if found and belongs to the user, None otherwise
        """
        try:
            statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
            result = await self.session.execute(statement)
            return result.scalar_one_or_none()
        except Exception as e:
            self.error_handler.handle_database_error(e, "Getting task by ID")
            raise

    async def verify_task_ownership(self, task_id: str, user_id: str) -> bool:
        """
        Verify that a specific task belongs to the specified user.

        Args:
            task_id: The ID of the task to verify ownership for
            user_id: The ID of the user claiming ownership

        Returns:
            True if the user owns the task, False otherwise
        """
        try:
            statement = select(Task.id).where(Task.id == task_id, Task.user_id == user_id)
            result = await self.session.execute(statement)
            task = result.scalar_one_or_none()
            return task is not None
        except Exception as e:
            self.error_handler.handle_database_error(e, "Verifying task ownership")
            return False

    async def get_task_owner(self, task_id: str) -> Optional[str]:
        """
        Get the owner user ID for a specific task.

        Args:
            task_id: The ID of the task to get owner for

        Returns:
            User ID of the task owner if found, None otherwise
        """
        try:
            statement = select(Task.user_id).where(Task.id == task_id)
            result = await self.session.execute(statement)
            return result.scalar_one_or_none()
        except Exception as e:
            self.error_handler.handle_database_error(e, "Getting task owner")
            raise

    async def create_task(self, title: str, description: Optional[str] = None,
                         is_completed: bool = False, user_id: str = None) -> Task:
        """
        Create a new task for a user.

        Args:
            title: Task title (required)
            description: Task description (optional)
            is_completed: Completion status (default: False)
            user_id: ID of the user creating the task

        Returns:
            Created Task object
        """
        try:
            db_task = Task(
                title=title,
                description=description,
                is_completed=is_completed,
                user_id=user_id
            )

            self.session.add(db_task)
            await self.session.commit()
            await self.session.refresh(db_task)
            return db_task
        except IntegrityError as e:
            self.error_handler.handle_database_error(e, "Creating task - integrity constraint violation")
            raise
        except Exception as e:
            self.error_handler.handle_database_error(e, "Creating task")
            raise

    async def update_task(self, task_id: str, user_id: str,
                         title: Optional[str] = None,
                         description: Optional[str] = None,
                         is_completed: Optional[bool] = None) -> Optional[Task]:
        """
        Update an existing task if it belongs to the user.

        Args:
            task_id: ID of the task to update
            user_id: ID of the user who owns the task
            title: New title (optional)
            description: New description (optional)
            is_completed: New completion status (optional)

        Returns:
            Updated Task object if successful, None if task not found or not owned by user
        """
        try:
            # First, verify the task exists and belongs to the user
            statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
            result = await self.session.execute(statement)
            db_task = result.scalar_one_or_none()

            if not db_task:
                return None

            # Update fields if provided
            if title is not None:
                db_task.title = title
            if description is not None:
                db_task.description = description
            if is_completed is not None:
                db_task.is_completed = is_completed

            db_task.updated_at = datetime.utcnow()

            await self.session.commit()
            await self.session.refresh(db_task)
            return db_task
        except IntegrityError as e:
            self.error_handler.handle_database_error(e, "Updating task - integrity constraint violation")
            raise
        except Exception as e:
            self.error_handler.handle_database_error(e, "Updating task")
            raise

    async def delete_task(self, task_id: str, user_id: str) -> bool:
        """
        Delete a task if it belongs to the user.

        Args:
            task_id: ID of the task to delete
            user_id: ID of the user who owns the task

        Returns:
            True if task was deleted, False if not found or not owned by user
        """
        try:
            statement = delete(Task).where(Task.id == task_id, Task.user_id == user_id)
            result = await self.session.execute(statement)

            if result.rowcount > 0:
                await self.session.commit()
                return True
            else:
                return False
        except Exception as e:
            self.error_handler.handle_database_error(e, "Deleting task")
            raise

    async def toggle_task_completion(self, task_id: str, user_id: str,
                                   is_completed: bool) -> Optional[Task]:
        """
        Toggle the completion status of a task.

        Args:
            task_id: ID of the task to update
            user_id: ID of the user who owns the task
            is_completed: New completion status

        Returns:
            Updated Task object if successful, None if task not found or not owned by user
        """
        try:
            # First, verify the task exists and belongs to the user
            statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
            result = await self.session.execute(statement)
            db_task = result.scalar_one_or_none()

            if not db_task:
                return None

            # Update the completion status
            db_task.is_completed = is_completed
            db_task.updated_at = datetime.utcnow()

            await self.session.commit()
            await self.session.refresh(db_task)
            return db_task
        except Exception as e:
            self.error_handler.handle_database_error(e, "Toggling task completion")
            raise

    async def get_tasks_by_completion_status(self, user_id: str,
                                           is_completed: bool) -> List[Task]:
        """
        Get tasks filtered by completion status for a specific user.

        Args:
            user_id: ID of the user whose tasks to retrieve
            is_completed: Completion status to filter by

        Returns:
            List of Task objects with the specified completion status
        """
        try:
            statement = select(Task).where(
                Task.user_id == user_id,
                Task.is_completed == is_completed
            ).order_by(Task.created_at.desc())

            result = await self.session.execute(statement)
            return result.scalars().all()
        except Exception as e:
            self.error_handler.handle_database_error(e, "Getting tasks by completion status")
            raise

    async def get_task_count_by_user(self, user_id: str) -> int:
        """
        Get the total count of tasks for a user.

        Args:
            user_id: ID of the user whose task count to retrieve

        Returns:
            Number of tasks belonging to the user
        """
        try:
            from sqlalchemy import func
            statement = select(func.count(Task.id)).where(Task.user_id == user_id)
            result = await self.session.execute(statement)
            return result.scalar_one()
        except Exception as e:
            self.error_handler.handle_database_error(e, "Getting task count by user")
            raise