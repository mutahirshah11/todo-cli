from typing import List, Optional
from src.todo_cli.services.task_service import TaskService
from src.todo_cli.models.task import Task as CliTask
from backend.api.models.task import TaskCreate, TaskUpdate, TaskToggle, TaskResponse


class TaskAdapter:
    """
    Adapter service to bridge the API layer with the existing CLI TaskService.
    This ensures the API uses the same business logic as the CLI while providing
    the necessary transformations between API models and CLI models.
    """

    def __init__(self, user_id: str):
        self.service = TaskService(user_id=user_id)

    def get_all_tasks(self) -> List[TaskResponse]:
        """Get all tasks for the user and convert to API response format."""
        cli_tasks = self.service.get_all_tasks()
        return [self._convert_cli_task_to_api_response(cli_task) for cli_task in cli_tasks]

    def get_task_by_id(self, task_id: int) -> Optional[TaskResponse]:
        """Get a specific task by ID and convert to API response format."""
        cli_task = self.service.get_task_by_id(task_id)
        if cli_task:
            return self._convert_cli_task_to_api_response(cli_task)
        return None

    def create_task(self, task_create: TaskCreate) -> TaskResponse:
        """Create a new task using the CLI service and convert to API response format."""
        cli_task = self.service.add_task(
            title=task_create.title,
            description=task_create.description
        )
        # Update the completed status after creation since add_task always sets it to False
        if task_create.completed:
            cli_task = self.service.mark_complete(cli_task.id)
        return self._convert_cli_task_to_api_response(cli_task)

    def update_task(self, task_id: int, task_update: TaskUpdate) -> Optional[TaskResponse]:
        """Update an existing task using the CLI service and convert to API response format."""
        # Use the current task's title/description as defaults if not provided in update
        current_task = self.service.get_task_by_id(task_id)
        if not current_task:
            return None

        # Use provided values or fall back to current values
        title = task_update.title if task_update.title is not None else current_task.title
        description = task_update.description if task_update.description is not None else current_task.description

        updated_cli_task = self.service.update_task(
            task_id=task_id,
            title=title,
            description=description
        )

        # Update completion status if provided in the update
        if updated_cli_task and task_update.completed is not None:
            if task_update.completed:
                updated_cli_task = self.service.mark_complete(task_id)
            else:
                updated_cli_task = self.service.mark_incomplete(task_id)

        if updated_cli_task:
            return self._convert_cli_task_to_api_response(updated_cli_task)
        return None

    def delete_task(self, task_id: int) -> bool:
        """Delete a task using the CLI service."""
        return self.service.delete_task(task_id)

    def toggle_completion(self, task_id: int, task_toggle: TaskToggle) -> Optional[TaskResponse]:
        """Toggle completion status of a task using the CLI service."""
        if task_toggle.completed:
            cli_task = self.service.mark_complete(task_id)
        else:
            cli_task = self.service.mark_incomplete(task_id)

        if cli_task:
            return self._convert_cli_task_to_api_response(cli_task)
        return None

    def _convert_cli_task_to_api_response(self, cli_task: CliTask) -> TaskResponse:
        """Convert a CLI Task to an API TaskResponse."""
        return TaskResponse(
            id=cli_task.id,
            title=cli_task.title,
            description=cli_task.description,
            completed=cli_task.completed,
            created_at=cli_task.created_at,
            updated_at=cli_task.updated_at,
            user_id=cli_task.user_id
        )