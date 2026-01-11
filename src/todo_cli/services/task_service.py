import json
import os
from typing import List, Optional, Dict, Any
from pathlib import Path
from datetime import datetime
from ..models.task import Task


class TaskService:
    """
    Service class for managing tasks with in-memory storage and temporary file persistence.
    """

    def __init__(self, user_id: str, storage_file: Optional[str] = None):
        """
        Initialize the TaskService with user_id and optional storage file.

        Args:
            user_id: The ID of the user this service is managing tasks for
            storage_file: Path to the temporary file for persistence.
                         Defaults to 'todo_data.json' in the current directory.
        """
        self.user_id = user_id
        # Use storage file from environment variable if set, otherwise default
        if storage_file is None:
            self.storage_file = os.environ.get('TODO_STORAGE_FILE', 'todo_data.json')
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
                    # Convert old format (with content) to new format (with title/description)
                    converted_tasks = []
                    for task_data in data:
                        # Create a copy to avoid modifying the original data
                        task_dict = task_data.copy()

                        if 'content' in task_dict and 'title' not in task_dict:
                            # Convert old format to new format
                            task_dict['title'] = task_dict.pop('content')
                            task_dict['description'] = ""

                        # Handle datetime conversion
                        if 'created_at' in task_dict and isinstance(task_dict['created_at'], str):
                            task_dict['created_at'] = datetime.fromisoformat(task_dict['created_at'])
                        if 'updated_at' in task_dict and isinstance(task_dict['updated_at'], str):
                            task_dict['updated_at'] = datetime.fromisoformat(task_dict['updated_at'])

                        # For old tasks without user_id, assign the current service's user_id
                        if 'user_id' not in task_dict or not task_dict['user_id']:
                            task_dict['user_id'] = self.user_id

                        converted_tasks.append(Task(**task_dict))

                    # Filter tasks by user_id and remove duplicates based on task ID
                user_tasks = [task for task in converted_tasks if task.user_id == self.user_id]

                # Use a dictionary to keep track of unique tasks by ID (keeps last occurrence)
                unique_tasks_map = {}
                for task in user_tasks:
                    unique_tasks_map[task.id] = task  # Overwrite duplicates, keeping latest

                # Convert back to list maintaining order of first occurrence but with latest data
                self.tasks = list(unique_tasks_map.values())
            except (json.JSONDecodeError, KeyError, ValueError, TypeError):
                # If file is corrupted or has wrong format, start with empty list
                self.tasks = []
        else:
            self.tasks = []

    def _save_to_file(self) -> None:
        """Save tasks to the temporary file."""
        # Load all tasks from file to maintain other users' data
        all_tasks_data = []
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    all_tasks_data = json.load(f)
            except (json.JSONDecodeError, KeyError, ValueError):
                all_tasks_data = []

        # Remove tasks belonging to this user from the list
        other_users_tasks = []
        for task_data in all_tasks_data:
            # Check if this task belongs to the current user
            task_user_id = task_data.get('user_id', 'default_user')  # Default for old tasks without user_id
            if task_user_id != self.user_id:
                other_users_tasks.append(task_data)

        # Add current user's tasks (converted to dict format)
        current_user_tasks = []
        for task in self.tasks:
            task_dict = {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "user_id": task.user_id,
                "created_at": task.created_at.isoformat() if hasattr(task.created_at, 'isoformat') else task.created_at,
                "updated_at": task.updated_at.isoformat() if hasattr(task.updated_at, 'isoformat') else task.updated_at
            }
            current_user_tasks.append(task_dict)

        # Combine all tasks
        all_tasks_json = other_users_tasks + current_user_tasks

        with open(self.storage_file, 'w', encoding='utf-8') as f:
            json.dump(all_tasks_json, f, ensure_ascii=False, indent=2)

    def add_task(self, title: str, description: str = "") -> Task:
        """
        Creates new Task with next sequential ID and adds to collection, persists to temporary file.

        Args:
            title: The title of the task
            description: The description of the task

        Returns:
            The created Task object
        """
        next_id = self._get_next_id()
        task = Task(
            id=next_id,
            title=title,
            description=description,
            completed=False,
            user_id=self.user_id
        )
        self.tasks.append(task)
        self._save_to_file()
        return task

    def get_all_tasks(self) -> List[Task]:
        """
        Returns all tasks for the current user.

        Returns:
            List of all tasks for the current user
        """
        return self.tasks.copy()  # Return a copy to prevent external modification

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """
        Returns specific task by ID for the current user or null if not found.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            The task if found, None otherwise
        """
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(self, task_id: int, title: str, description: str = "") -> Optional[Task]:
        """
        Updates title and description of existing task for the current user, persists to temporary file.

        Args:
            task_id: The ID of the task to update
            title: The new title for the task
            description: The new description for the task

        Returns:
            The updated task if found, None otherwise
        """
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                self.tasks[i] = Task(
                    id=task.id,
                    title=title,
                    description=description,
                    completed=task.completed,
                    user_id=task.user_id,
                    created_at=task.created_at,
                    updated_at=datetime.now()
                )
                self._save_to_file()
                return self.tasks[i]
        return None

    def delete_task(self, task_id: int) -> bool:
        """
        Removes task from collection for the current user, persists to temporary file.

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
                self.tasks[i] = Task(
                    id=task.id,
                    title=task.title,
                    description=task.description,
                    completed=True,
                    user_id=task.user_id,
                    created_at=task.created_at,
                    updated_at=datetime.now()
                )
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
                self.tasks[i] = Task(
                    id=task.id,
                    title=task.title,
                    description=task.description,
                    completed=False,
                    user_id=task.user_id,
                    created_at=task.created_at,
                    updated_at=datetime.now()
                )
                self._save_to_file()
                return self.tasks[i]
        return None

    def toggle_completion(self, task_id: int) -> Optional[Task]:
        """
        Toggles completion status of a task, persists to temporary file.

        Args:
            task_id: The ID of the task to toggle

        Returns:
            The updated task if found, None otherwise
        """
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                new_completed_status = not task.completed
                self.tasks[i] = Task(
                    id=task.id,
                    title=task.title,
                    description=task.description,
                    completed=new_completed_status,
                    user_id=task.user_id,
                    created_at=task.created_at,
                    updated_at=datetime.now()
                )
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