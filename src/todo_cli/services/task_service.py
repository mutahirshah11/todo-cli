import json
import os
from typing import List, Optional, Dict, Any
from pathlib import Path
from ..models.task import Task


class TaskService:
    """
    Service class for managing tasks with in-memory storage and temporary file persistence.
    """

    def __init__(self, storage_file: Optional[str] = None):
        """
        Initialize the TaskService with optional storage file.

        Args:
            storage_file: Path to the temporary file for persistence.
                         Defaults to 'todo_data.json' in the current directory.
        """
        # Use storage file from environment variable if set, otherwise default
        if storage_file is None:
            self.storage_file = os.environ.get('TODO_STORAGE_FILE', os.path.join(os.path.expanduser("~"), ".todo_data.json"))
        else:
            self.storage_file = storage_file
        self.tasks: List[Task] = []
        self._load_from_file()

    def _load_from_file(self) -> None:
        """Load tasks from the temporary file if it exists."""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.tasks = [Task(**task_data) for task_data in data]
            except (json.JSONDecodeError, KeyError, ValueError):
                # If file is corrupted or has wrong format, start with empty list
                self.tasks = []
        else:
            self.tasks = []

    def _save_to_file(self) -> None:
        """Save tasks to the temporary file."""
        tasks_data = [
            {
                "id": task.id,
                "content": task.content,
                "completed": task.completed
            }
            for task in self.tasks
        ]
        with open(self.storage_file, 'w', encoding='utf-8') as f:
            json.dump(tasks_data, f, ensure_ascii=False, indent=2)

    def add_task(self, content: str) -> Task:
        """
        Creates new Task with next sequential ID and adds to collection, persists to temporary file.

        Args:
            content: The content of the task

        Returns:
            The created Task object
        """
        next_id = self._get_next_id()
        task = Task(id=next_id, content=content, completed=False)
        self.tasks.append(task)
        self._save_to_file()
        return task

    def get_all_tasks(self) -> List[Task]:
        """
        Loads tasks from temporary file, returns all tasks in collection.

        Returns:
            List of all tasks
        """
        self._load_from_file()
        return self.tasks.copy()  # Return a copy to prevent external modification

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """
        Loads tasks from temporary file, returns specific task by ID or null if not found.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            The task if found, None otherwise
        """
        self._load_from_file()
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(self, task_id: int, content: str) -> Optional[Task]:
        """
        Updates content of existing task, persists to temporary file.

        Args:
            task_id: The ID of the task to update
            content: The new content for the task

        Returns:
            The updated task if found, None otherwise
        """
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                self.tasks[i] = Task(id=task.id, content=content, completed=task.completed)
                self._save_to_file()
                return self.tasks[i]
        return None

    def delete_task(self, task_id: int) -> bool:
        """
        Removes task from collection, persists to temporary file.

        Args:
            task_id: The ID of the task to delete

        Returns:
            True if task was deleted, False if not found
        """
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                del self.tasks[i]
                self._save_to_file()
                return True
        return False

    def mark_complete(self, task_id: int) -> Optional[Task]:
        """
        Updates completion status to true, persists to temporary file.

        Args:
            task_id: The ID of the task to mark as complete

        Returns:
            The updated task if found, None otherwise
        """
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                self.tasks[i] = Task(id=task.id, content=task.content, completed=True)
                self._save_to_file()
                return self.tasks[i]
        return None

    def mark_incomplete(self, task_id: int) -> Optional[Task]:
        """
        Updates completion status to false, persists to temporary file.

        Args:
            task_id: The ID of the task to mark as incomplete

        Returns:
            The updated task if found, None otherwise
        """
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                self.tasks[i] = Task(id=task.id, content=task.content, completed=False)
                self._save_to_file()
                return self.tasks[i]
        return None

    def _get_next_id(self) -> int:
        """
        Get the next sequential ID for a new task.

        Returns:
            The next available ID
        """
        if not self.tasks:
            return 1
        # Find the highest ID and add 1
        max_id = max((task.id for task in self.tasks), default=0)
        return max_id + 1