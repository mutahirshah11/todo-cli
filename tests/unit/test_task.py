import pytest
from src.todo_cli.models.task import Task


class TestTaskModel:
    """Tests for the Task model."""

    def test_task_creation_success(self):
        """Test successful creation of a task with valid data."""
        task = Task(id=1, content="Test task", completed=False)

        assert task.id == 1
        assert task.content == "Test task"
        assert task.completed is False

    def test_task_creation_defaults(self):
        """Test that completed defaults to False."""
        task = Task(id=1, content="Test task")

        assert task.id == 1
        assert task.content == "Test task"
        assert task.completed is False

    def test_task_creation_completed_true(self):
        """Test creation of a completed task."""
        task = Task(id=1, content="Test task", completed=True)

        assert task.id == 1
        assert task.content == "Test task"
        assert task.completed is True

    def test_task_id_validation_negative(self):
        """Test that negative ID raises ValueError."""
        with pytest.raises(ValueError, match="Task ID must be a positive integer"):
            Task(id=-1, content="Test task")

    def test_task_id_validation_zero(self):
        """Test that zero ID raises ValueError."""
        with pytest.raises(ValueError, match="Task ID must be a positive integer"):
            Task(id=0, content="Test task")

    def test_task_content_validation_empty(self):
        """Test that empty content raises ValueError."""
        with pytest.raises(ValueError, match="Task content must be a non-empty string"):
            Task(id=1, content="")

    def test_task_content_validation_none(self):
        """Test that None content raises ValueError."""
        with pytest.raises(ValueError, match="Task content must be a non-empty string"):
            Task(id=1, content=None)

    def test_task_content_validation_not_string(self):
        """Test that non-string content raises ValueError."""
        with pytest.raises(ValueError, match="Task content must be a non-empty string"):
            Task(id=1, content=123)

    def test_task_completed_validation_non_boolean(self):
        """Test that non-boolean completed value raises ValueError."""
        with pytest.raises(ValueError, match="Task completed status must be a boolean"):
            Task(id=1, content="Test task", completed="true")

    def test_task_equality(self):
        """Test task equality comparison."""
        task1 = Task(id=1, content="Test task", completed=False)
        task2 = Task(id=1, content="Test task", completed=False)

        assert task1 == task2

    def test_task_inequality_different_id(self):
        """Test task inequality with different IDs."""
        task1 = Task(id=1, content="Test task", completed=False)
        task2 = Task(id=2, content="Test task", completed=False)

        assert task1 != task2

    def test_task_inequality_different_content(self):
        """Test task inequality with different content."""
        task1 = Task(id=1, content="Test task 1", completed=False)
        task2 = Task(id=1, content="Test task 2", completed=False)

        assert task1 != task2

    def test_task_inequality_different_completed(self):
        """Test task inequality with different completed status."""
        task1 = Task(id=1, content="Test task", completed=False)
        task2 = Task(id=1, content="Test task", completed=True)

        assert task1 != task2