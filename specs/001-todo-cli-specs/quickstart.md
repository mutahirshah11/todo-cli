# Quickstart: Todo CLI Application

## Prerequisites

- Python 3.11 or higher
- `uv` package manager installed

## Installation

1. Install `uv` package manager:
   ```bash
   pip install uv
   # Or install via other methods as per uv documentation
   ```

2. Create a new project directory and navigate to it:
   ```bash
   mkdir todo-cli-app
   cd todo-cli-app
   ```

3. Initialize the project with uv:
   ```bash
   uv init
   ```

4. Add dependencies:
   ```bash
   uv add click pytest
   ```

## Project Structure

```
todo-cli-app/
├── pyproject.toml          # Project configuration and dependencies
├── src/
│   └── todo_cli/
│       ├── __init__.py
│       ├── main.py         # CLI entry point
│       ├── models/
│       │   ├── __init__.py
│       │   └── task.py     # Task data model
│       ├── services/
│       │   ├── __init__.py
│       │   └── task_service.py  # Task operations logic
│       └── cli/
│           ├── __init__.py
│           └── commands.py   # CLI command definitions
├── tests/
│   ├── unit/
│   ├── integration/
│   └── contract/
└── README.md
```

## Basic Usage

After implementation, the application will support these commands:

```bash
# Add a new task
todo add "Buy groceries"

# List all tasks
todo list

# Mark a task as complete
todo complete 1

# Update a task
todo update 1 "Buy groceries and cat food"

# Delete a task
todo delete 1

# Get help
todo --help
```

## Development Commands

```bash
# Run tests
uv run pytest

# Run the application
uv run python -m todo_cli.main

# Format code
uv run black src/

# Check for linting issues
uv run flake8 src/
```

## Output Formats

The application supports both human-readable and JSON output formats:

```bash
# Human-readable format (default)
todo list

# JSON format
todo list --json
```

## State Persistence

The application maintains state between command executions using a temporary file. Tasks will persist between different CLI commands during the same session, but will be lost when the system is restarted.