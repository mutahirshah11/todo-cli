import os
import tempfile
import json
import pytest
from src.todo_cli.models.task import Task
from src.todo_cli.services.task_service import TaskService


class TestTaskService:
    """Tests for the TaskService class."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        # Create a temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_file.close()
        self.service = TaskService(storage_file=self.temp_file.name)

    def teardown_method(self):
        """Clean up after each test method."""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)

    def test_add_task_success(self):
        """Test adding a task successfully."""
        task = self.service.add_task("Test task")

        assert task.id == 1
        assert task.content == "Test task"
        assert task.completed is False

        # Verify the task was saved to file
        tasks = self.service.get_all_tasks()
        assert len(tasks) == 1
        assert tasks[0].id == 1
        assert tasks[0].content == "Test task"
        assert tasks[0].completed is False

    def test_add_multiple_tasks_sequential_ids(self):
        """Test that multiple tasks get sequential IDs."""
        task1 = self.service.add_task("First task")
        task2 = self.service.add_task("Second task")
        task3 = self.service.add_task("Third task")

        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3

    def test_get_all_tasks_empty(self):
        """Test getting all tasks when the list is empty."""
        tasks = self.service.get_all_tasks()

        assert tasks == []

    def test_get_all_tasks_with_data(self):
        """Test getting all tasks when there is data."""
        self.service.add_task("First task")
        self.service.add_task("Second task")

        tasks = self.service.get_all_tasks()

        assert len(tasks) == 2
        assert tasks[0].id == 1
        assert tasks[0].content == "First task"
        assert tasks[1].id == 2
        assert tasks[1].content == "Second task"

    def test_get_task_by_id_exists(self):
        """Test getting a task by ID when it exists."""
        self.service.add_task("Test task")
        task = self.service.get_task_by_id(1)

        assert task is not None
        assert task.id == 1
        assert task.content == "Test task"
        assert task.completed is False

    def test_get_task_by_id_not_exists(self):
        """Test getting a task by ID when it doesn't exist."""
        task = self.service.get_task_by_id(999)

        assert task is None

    def test_update_task_success(self):
        """Test updating a task successfully."""
        self.service.add_task("Original task")
        updated_task = self.service.update_task(1, "Updated task")

        assert updated_task is not None
        assert updated_task.id == 1
        assert updated_task.content == "Updated task"
        assert updated_task.completed is False  # Should preserve completion status

    def test_update_task_not_exists(self):
        """Test updating a task that doesn't exist."""
        result = self.service.update_task(999, "Updated task")

        assert result is None

    def test_delete_task_success(self):
        """Test deleting a task successfully."""
        self.service.add_task("Test task")
        success = self.service.delete_task(1)

        assert success is True

        # Verify the task was deleted
        tasks = self.service.get_all_tasks()
        assert len(tasks) == 0

    def test_delete_task_not_exists(self):
        """Test deleting a task that doesn't exist."""
        success = self.service.delete_task(999)

        assert success is False

    def test_mark_complete_success(self):
        """Test marking a task as complete."""
        self.service.add_task("Test task")
        task = self.service.mark_complete(1)

        assert task is not None
        assert task.id == 1
        assert task.completed is True

    def test_mark_complete_not_exists(self):
        """Test marking a task as complete when it doesn't exist."""
        result = self.service.mark_complete(999)

        assert result is None

    def test_mark_incomplete_success(self):
        """Test marking a task as incomplete."""
        self.service.add_task("Test task")
        # First mark it complete
        completed_task = self.service.mark_complete(1)
        # Then mark it incomplete
        incomplete_task = self.service.mark_incomplete(1)

        assert incomplete_task is not None
        assert incomplete_task.id == 1
        assert incomplete_task.completed is False

    def test_mark_incomplete_not_exists(self):
        """Test marking a task as incomplete when it doesn't exist."""
        result = self.service.mark_incomplete(999)

        assert result is None

    def test_file_persistence(self):
        """Test that tasks are persisted to and loaded from file."""
        # Add tasks to service
        self.service.add_task("First task")
        self.service.add_task("Second task")

        # Create a new service instance with the same file
        new_service = TaskService(storage_file=self.temp_file.name)
        tasks = new_service.get_all_tasks()

        assert len(tasks) == 2
        assert tasks[0].id == 1
        assert tasks[0].content == "First task"
        assert tasks[1].id == 2
        assert tasks[1].content == "Second task"

    def test_file_corruption_handling(self):
        """Test that service handles corrupted files gracefully."""
        # Write corrupted data to the file
        with open(self.temp_file.name, 'w') as f:
            f.write("This is not valid JSON")

        # Create a new service - should handle the corrupted file
        new_service = TaskService(storage_file=self.temp_file.name)
        tasks = new_service.get_all_tasks()

        # Should return empty list for corrupted file
        assert tasks == []

    def test_load_from_nonexistent_file(self):
        """Test loading from a file that doesn't exist."""
        # Create a temporary file path without creating the file
        temp_file_path = tempfile.mktemp(suffix='.json')

        service = TaskService(storage_file=temp_file_path)
        tasks = service.get_all_tasks()

        # Should return empty list
        assert tasks == []

        # Clean up
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

    def test_get_next_id_empty_list(self):
        """Test that next ID is 1 when list is empty."""
        # All tasks were deleted, so list should be empty
        tasks = self.service.get_all_tasks()
        for task in tasks:
            self.service.delete_task(task.id)

        # Add a new task - should get ID 1
        task = self.service.add_task("New task")
        assert task.id == 1

    def test_get_next_id_with_gaps(self):
        """Test that next ID is based on max ID + 1, not counting."""
        self.service.add_task("Task 1")
        self.service.add_task("Task 2")
        self.service.add_task("Task 3")
        self.service.delete_task(2)  # Delete middle task, creating a gap

        task = self.service.add_task("New task")
        assert task.id == 4  # Should be max_id + 1 = 3 + 1 = 4