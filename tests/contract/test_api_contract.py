import subprocess
import sys
import json
import tempfile
import os


# Global temporary file for all contract tests to ensure consistency
CONTRACT_TEST_FILE = os.path.join(tempfile.gettempdir(), "contract_test_todo_data.json")


def run_cli_command(args):
    """Helper function to run CLI commands and capture output."""
    cmd = [sys.executable, "-m", "src.todo_cli.main"] + args

    # Set up environment with temporary file for consistency
    env = os.environ.copy()
    # Use a consistent temporary file for all contract tests
    env['TODO_STORAGE_FILE'] = CONTRACT_TEST_FILE

    result = subprocess.run(
        cmd,
        text=True,
        capture_output=True,
        env=env
    )
    return result


class TestAPIContract:
    """Contract tests for CLI API based on specifications."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        # Clear the test file to ensure a clean state
        if os.path.exists(CONTRACT_TEST_FILE):
            os.remove(CONTRACT_TEST_FILE)

    def test_add_command_contract(self):
        """Test add command contract: todo add 'task content'."""
        result = run_cli_command(["add", "Test contract task"])

        # Should return exit code 0 on success
        assert result.returncode == 0
        # Should provide success message
        assert "Task added successfully" in result.stdout

    def test_add_command_json_contract(self):
        """Test add command JSON output contract."""
        result = run_cli_command(["add", "Test JSON task", "--json"])

        # Should return exit code 0 on success
        assert result.returncode == 0
        # Should provide valid JSON output
        try:
            output = json.loads(result.stdout)
            assert "success" in output
            assert output["success"] is True
            assert "task" in output
        except json.JSONDecodeError:
            assert False, f"Invalid JSON output: {result.stdout}"

    def test_list_command_contract(self):
        """Test list command contract: todo list."""
        # First add a task
        add_result = run_cli_command(["add", "List contract test"])
        assert add_result.returncode == 0

        # Then list tasks
        result = run_cli_command(["list"])

        # Should return exit code 0 on success
        assert result.returncode == 0
        # Should show the task in the list
        assert "List contract test" in result.stdout

    def test_list_command_json_contract(self):
        """Test list command JSON output contract."""
        # First add a task
        add_result = run_cli_command(["add", "JSON list test"])
        assert add_result.returncode == 0

        # Then list tasks with JSON output
        result = run_cli_command(["list", "--json"])

        # Should return exit code 0 on success
        assert result.returncode == 0
        # Should provide valid JSON output
        try:
            output = json.loads(result.stdout)
            assert "tasks" in output
            assert isinstance(output["tasks"], list)
        except json.JSONDecodeError:
            assert False, f"Invalid JSON output: {result.stdout}"

    def test_complete_command_contract(self):
        """Test complete command contract: todo complete [id]."""
        # First add a task
        add_result = run_cli_command(["add", "Complete contract test"])
        assert add_result.returncode == 0

        # Then mark it complete
        result = run_cli_command(["complete", "1"])

        # Should return exit code 0 on success
        assert result.returncode == 0
        # Should provide success message
        assert "marked as complete" in result.stdout

    def test_complete_command_error_contract(self):
        """Test complete command error handling contract."""
        # Try to complete a non-existent task
        result = run_cli_command(["complete", "999"])

        # Should return exit code 2 for invalid ID
        assert result.returncode == 2

    def test_update_command_contract(self):
        """Test update command contract: todo update [id] 'new content'."""
        # First add a task
        add_result = run_cli_command(["add", "Original content"])
        assert add_result.returncode == 0

        # Then update it
        result = run_cli_command(["update", "1", "Updated content"])

        # Should return exit code 0 on success
        assert result.returncode == 0
        # Should provide success message
        assert "updated successfully" in result.stdout

    def test_update_command_error_contract(self):
        """Test update command error handling contract."""
        # Try to update a non-existent task
        result = run_cli_command(["update", "999", "New content"])

        # Should return exit code 2 for invalid ID
        assert result.returncode == 2

    def test_delete_command_contract(self):
        """Test delete command contract: todo delete [id]."""
        # First add a task
        add_result = run_cli_command(["add", "Delete contract test"])
        assert add_result.returncode == 0

        # Then delete it
        result = run_cli_command(["delete", "1"])

        # Should return exit code 0 on success
        assert result.returncode == 0
        # Should provide success message
        assert "deleted successfully" in result.stdout

    def test_delete_command_error_contract(self):
        """Test delete command error handling contract."""
        # Try to delete a non-existent task
        result = run_cli_command(["delete", "999"])

        # Should return exit code 2 for invalid ID
        assert result.returncode == 2

    def test_command_help_contract(self):
        """Test that commands provide help information."""
        result = run_cli_command(["--help"])

        # Should return exit code 0
        assert result.returncode == 0
        # Should contain usage information
        assert "Usage:" in result.stdout