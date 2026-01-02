import os
import tempfile
import json
import subprocess
import sys
from pathlib import Path


def run_cli_command(args, input_data=None):
    """Helper function to run CLI commands and capture output."""
    # Get the path to the main module
    cmd = [sys.executable, "-m", "src.todo_cli.main"] + args

    # Set up environment with temporary file
    env = os.environ.copy()

    result = subprocess.run(
        cmd,
        input=input_data,
        text=True,
        capture_output=True,
        env=env
    )
    return result


class TestCLIBasicCommands:
    """Integration tests for CLI commands."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        # Create a temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_file.close()

        # Set the storage file environment or use default
        self.original_storage = os.environ.get('TODO_STORAGE_FILE')
        os.environ['TODO_STORAGE_FILE'] = self.temp_file.name

    def teardown_method(self):
        """Clean up after each test method."""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)

        if self.original_storage is not None:
            os.environ['TODO_STORAGE_FILE'] = self.original_storage
        elif 'TODO_STORAGE_FILE' in os.environ:
            del os.environ['TODO_STORAGE_FILE']

    def test_add_command_basic(self):
        """Test the add command works correctly."""
        result = run_cli_command(["add", "Test task content"])

        assert result.returncode == 0
        assert "Task added successfully" in result.stdout

    def test_add_command_json_output(self):
        """Test the add command with JSON output."""
        result = run_cli_command(["add", "Test task content", "--json"])

        assert result.returncode == 0
        try:
            output = json.loads(result.stdout)
            assert output["success"] is True
            assert "task" in output
            assert output["task"]["content"] == "Test task content"
        except json.JSONDecodeError:
            assert False, f"Invalid JSON output: {result.stdout}"

    def test_list_command_empty(self):
        """Test the list command when no tasks exist."""
        result = run_cli_command(["list"])

        assert result.returncode == 0
        assert "No tasks in the list" in result.stdout

    def test_list_command_with_tasks(self):
        """Test the list command with existing tasks."""
        # Add a task first
        add_result = run_cli_command(["add", "First task"])
        assert add_result.returncode == 0

        add_result = run_cli_command(["add", "Second task"])
        assert add_result.returncode == 0

        # Now list tasks
        result = run_cli_command(["list"])

        assert result.returncode == 0
        assert "First task" in result.stdout
        assert "Second task" in result.stdout

    def test_list_command_json_output(self):
        """Test the list command with JSON output."""
        # Add a task first
        add_result = run_cli_command(["add", "Test task"])
        assert add_result.returncode == 0

        # Now list tasks in JSON
        result = run_cli_command(["list", "--json"])

        assert result.returncode == 0
        try:
            output = json.loads(result.stdout)
            assert "tasks" in output
            assert len(output["tasks"]) == 1
            assert output["tasks"][0]["content"] == "Test task"
        except json.JSONDecodeError:
            assert False, f"Invalid JSON output: {result.stdout}"

    def test_complete_command_success(self):
        """Test the complete command works for existing tasks."""
        # Add a task first
        add_result = run_cli_command(["add", "Test task"])
        assert add_result.returncode == 0

        # Mark it as complete
        result = run_cli_command(["complete", "1"])

        assert result.returncode == 0
        assert "marked as complete" in result.stdout

    def test_complete_command_invalid_id(self):
        """Test the complete command fails for non-existent tasks."""
        result = run_cli_command(["complete", "999"])

        assert result.returncode == 2  # Error code 2 for invalid ID
        assert "not found" in result.stderr or "not found" in result.stdout

    def test_complete_command_json_output(self):
        """Test the complete command with JSON output."""
        # Add a task first
        add_result = run_cli_command(["add", "Test task"])
        assert add_result.returncode == 0

        # Mark it as complete with JSON output
        result = run_cli_command(["complete", "1", "--json"])

        assert result.returncode == 0
        try:
            output = json.loads(result.stdout)
            assert output["success"] is True
            assert output["task"]["completed"] is True
        except json.JSONDecodeError:
            assert False, f"Invalid JSON output: {result.stdout}"

    def test_update_command_success(self):
        """Test the update command works for existing tasks."""
        # Add a task first
        add_result = run_cli_command(["add", "Original task"])
        assert add_result.returncode == 0

        # Update the task
        result = run_cli_command(["update", "1", "Updated task"])

        assert result.returncode == 0
        assert "updated successfully" in result.stdout

    def test_update_command_invalid_id(self):
        """Test the update command fails for non-existent tasks."""
        result = run_cli_command(["update", "999", "Updated task"])

        assert result.returncode == 2  # Error code 2 for invalid ID
        assert "not found" in result.stderr or "not found" in result.stdout

    def test_delete_command_success(self):
        """Test the delete command works for existing tasks."""
        # Add a task first
        add_result = run_cli_command(["add", "Test task"])
        assert add_result.returncode == 0

        # Delete the task
        result = run_cli_command(["delete", "1"])

        assert result.returncode == 0
        assert "deleted successfully" in result.stdout

    def test_delete_command_invalid_id(self):
        """Test the delete command fails for non-existent tasks."""
        result = run_cli_command(["delete", "999"])

        assert result.returncode == 2  # Error code 2 for invalid ID
        assert "not found" in result.stderr or "not found" in result.stdout

    def test_command_help(self):
        """Test that help command works."""
        result = run_cli_command(["--help"])

        assert result.returncode == 0
        assert "Usage:" in result.stdout
        assert "add" in result.stdout
        assert "list" in result.stdout
        assert "complete" in result.stdout

    def test_error_handling_invalid_command(self):
        """Test error handling for invalid commands."""
        result = run_cli_command(["invalidcommand"])

        # Should return non-zero exit code for invalid command
        assert result.returncode != 0


class TestCLIDataPersistence:
    """Integration tests for data persistence across CLI commands."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        # Create a temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_file.close()

        # Set the storage file environment or use default
        self.original_storage = os.environ.get('TODO_STORAGE_FILE')
        os.environ['TODO_STORAGE_FILE'] = self.temp_file.name

    def teardown_method(self):
        """Clean up after each test method."""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)

        if self.original_storage is not None:
            os.environ['TODO_STORAGE_FILE'] = self.original_storage
        elif 'TODO_STORAGE_FILE' in os.environ:
            del os.environ['TODO_STORAGE_FILE']

    def test_persistence_across_commands(self):
        """Test that tasks persist between different CLI command executions."""
        # Add a task
        add_result = run_cli_command(["add", "Persistent task"])
        assert add_result.returncode == 0

        # List tasks - should show the added task
        list_result = run_cli_command(["list"])
        assert list_result.returncode == 0
        assert "Persistent task" in list_result.stdout

        # Complete the task
        complete_result = run_cli_command(["complete", "1"])
        assert complete_result.returncode == 0

        # List tasks again - should show the task as completed
        list_result2 = run_cli_command(["list"])
        assert list_result2.returncode == 0
        assert "Persistent task" in list_result2.stdout
        # Check that it's marked as completed (X)
        assert "X" in list_result2.stdout