# Todo CLI Application

A command-line todo application with in-memory storage and temporary file persistence between command executions.

## Features

- Add, delete, update, view, and mark tasks as complete
- Support for both human-readable and JSON output formats
- Sequential task ID assignment
- Temporary file persistence between command executions
- Standardized error codes and exit codes

## Installation

1. Ensure you have Python 3.11+ installed
2. Install the required dependencies:
   ```bash
   pip install click pytest
   ```

## Usage

### Basic Commands

```bash
# Add a new task
python -m src.todo_cli.main add "Buy groceries"

# List all tasks
python -m src.todo_cli.main list

# Mark a task as complete
python -m src.todo_cli.main complete 1

# Update a task
python -m src.todo_cli.main update 1 "Buy groceries and cat food"

# Delete a task
python -m src.todo_cli.main delete 1
```

### JSON Output

All commands support JSON output with the `--json` flag:

```bash
# Get JSON output
python -m src.todo_cli.main list --json
python -m src.todo_cli.main add "New task" --json
```

### Help

```bash
# Get help
python -m src.todo_cli.main --help
python -m src.todo_cli.main add --help
```

## MCP Server (For AI Agents)

The project includes an MCP (Model Context Protocol) server to allow AI agents to manage tasks.

### Prerequisites
- Python 3.12+
- `mcp` package installed
- Local PostgreSQL (Neon) or connection string

### Running the MCP Server
```bash
# Set environment variables
export NEON_DATABASE_URL="postgresql://..."

# Run the server (Stdio mode)
python backend/mcp_server.py
```

### Integrating with Claude Desktop / Agents
Add the following to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "todo-backend": {
      "command": "python",
      "args": ["/absolute/path/to/project/backend/mcp_server.py"],
      "env": {
        "NEON_DATABASE_URL": "postgresql://..."
      }
    }
  }
}
```

## Error Codes

- `0`: Success
- `1`: General error
- `2`: Invalid task ID
- `3`: Missing argument

## Project Structure

```
src/
├── todo_cli/
│   ├── __init__.py
│   ├── main.py          # CLI entry point
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py      # Task data model
│   ├── services/
│   │   ├── __init__.py
│   │   └── task_service.py  # Task operations logic
│   └── cli/
│       ├── __init__.py
│       └── commands.py    # CLI command definitions
backend/
├── mcp_server.py           # MCP Server entry point
├── api/
│   ├── mcp/                # MCP specific logic
tests/
├── unit/
│   ├── test_task.py
│   └── test_task_service.py
├── integration/
│   └── test_cli_commands.py
└── contract/
    └── test_api_contract.py
```

## Development

### Running Tests

```bash
# Run all tests
python -m pytest

# Run specific test files
python -m pytest tests/unit/
python -m pytest tests/integration/
python -m pytest tests/contract/

# Run MCP tests
$env:PYTHONPATH=".;backend"; pytest backend/tests/mcp
```

### Storage

The application uses temporary file persistence to maintain state between command executions. By default, tasks are stored in `~/.todo_data.json` (in the user's home directory). You can override this location using the `TODO_STORAGE_FILE` environment variable.

## Architecture

- **Task Model**: Represents a single todo item with ID, content, and completion status
- **TaskService**: Handles all business logic for task operations with persistence
- **CLI Commands**: Provides the command-line interface using the Click library
- **MCP Server**: Exposes task operations as tools for AI agents using the Official MCP SDK
