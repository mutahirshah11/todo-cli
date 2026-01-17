from typing import List, Optional
from api.models.task import TaskCreate, TaskUpdate, TaskToggle, TaskResponse
from api.repositories.task_repository import TaskRepository
from api.repositories.user_repository import UserRepository
from api.validation.task_validation import validate_task_create_model, validate_task_update_model, validate_task_toggle_model
from datetime import datetime


class TaskAdapter:
    """
    Adapter service to bridge the API layer with the database repositories.
    This ensures the API uses the database for persistent storage while providing
    the necessary transformations between API models and database models.
    """

    def __init__(self, session, user_id: str):
        self.session = session
        self.task_repo = TaskRepository(session)
        self.user_repo = UserRepository(session)
        self.user_id = user_id

    async def get_all_tasks(self) -> List[TaskResponse]:
        """Get all tasks for the user and convert to API response format."""
        db_tasks = await self.task_repo.get_tasks_by_user(self.user_id)
        return [self._convert_db_task_to_api_response(db_task) for db_task in db_tasks]

    async def get_task_by_id(self, task_id: str) -> Optional[TaskResponse]:
        """Get a specific task by ID and convert to API response format."""
        # Verify ownership first
        has_ownership = await self.task_repo.verify_task_ownership(task_id, self.user_id)
        if not has_ownership:
            return None

        db_task = await self.task_repo.get_task_by_id(task_id, self.user_id)
        if db_task:
            return self._convert_db_task_to_api_response(db_task)
        return None

    async def create_task(self, task_create: TaskCreate) -> TaskResponse:
        """Create a new task using the database repository and convert to API response format."""
        # Ensure the user exists in the backend database before creating the task
        await self._ensure_user_exists()

        # Validate the task creation request according to console app rules
        validated_task_create = validate_task_create_model(task_create)

        db_task = await self.task_repo.create_task(
            title=validated_task_create.title,
            description=validated_task_create.description,
            is_completed=validated_task_create.completed,
            user_id=self.user_id
        )
        return self._convert_db_task_to_api_response(db_task)

    async def _ensure_user_exists(self):
        """Ensure the user exists in the backend database, create if not."""
        # Check if user exists in backend database
        user_exists = await self.user_repo.user_exists(self.user_id)

        if not user_exists:
            # Create a minimal user record in the backend database with the specific user_id
            # Since we don't have the user's name and email here, we'll use a placeholder
            # In a real scenario, you'd want to fetch this from the auth service
            try:
                # Create a new user with the specific user_id
                db_user = await self.user_repo.create_user_if_not_exists(
                    user_id=self.user_id,
                    name=f"User_{self.user_id[:8]}",  # Take first 8 chars of user_id as name
                    email=f"{self.user_id}@placeholder.com"  # Placeholder email
                )
            except Exception as e:
                # Log the error but continue with the task creation
                print(f"Warning: Could not create user in backend: {e}")
                # Re-raise to ensure we don't create a task for a non-existent user
                raise

    async def update_task(self, task_id: str, task_update: TaskUpdate) -> Optional[TaskResponse]:
        """Update an existing task using the database repository and convert to API response format."""
        # Verify ownership first
        has_ownership = await self.task_repo.verify_task_ownership(task_id, self.user_id)
        if not has_ownership:
            return None

        # Validate the task update request according to console app rules
        validated_task_update = validate_task_update_model(task_update)

        updated_db_task = await self.task_repo.update_task(
            task_id=task_id,
            user_id=self.user_id,
            title=validated_task_update.title,
            description=validated_task_update.description,
            is_completed=validated_task_update.completed
        )

        if updated_db_task:
            return self._convert_db_task_to_api_response(updated_db_task)
        return None

    async def delete_task(self, task_id: str) -> bool:
        """Delete a task using the database repository."""
        # Verify ownership first
        has_ownership = await self.task_repo.verify_task_ownership(task_id, self.user_id)
        if not has_ownership:
            return False

        return await self.task_repo.delete_task(task_id, self.user_id)

    async def toggle_completion(self, task_id: str, task_toggle: TaskToggle) -> Optional[TaskResponse]:
        """Toggle completion status of a task using the database repository."""
        # Verify ownership first
        has_ownership = await self.task_repo.verify_task_ownership(task_id, self.user_id)
        if not has_ownership:
            return None

        # Validate the task toggle request according to console app rules
        validated_task_toggle = validate_task_toggle_model(task_toggle)

        updated_db_task = await self.task_repo.toggle_task_completion(task_id, self.user_id, validated_task_toggle.completed)

        if updated_db_task:
            return self._convert_db_task_to_api_response(updated_db_task)
        return None

    def _convert_db_task_to_api_response(self, db_task) -> TaskResponse:
        """Convert a database Task to an API TaskResponse."""
        return TaskResponse(
            id=db_task.id,
            title=db_task.title,
            description=db_task.description,
            completed=db_task.is_completed,
            created_at=db_task.created_at,
            updated_at=db_task.updated_at,
            user_id=db_task.user_id
        )