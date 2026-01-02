# API Contracts: Todo CLI Application

## CLI Command Contracts

### Add Command
- **Command**: `todo add "task content"`
- **Input**: Task content as string argument
- **Output**: Success message with task ID in both human-readable and JSON format
- **Exit Code**: 0 on success, non-zero on error
- **Error Codes**: 1 for general error, 3 for missing argument
- **Persistence**: Task is saved to temporary file and persists between command executions

### List Command
- **Command**: `todo list`
- **Input**: Optional `--json` flag for JSON output
- **Output**: List of all tasks with ID, content, and completion status
- **Exit Code**: 0 on success, non-zero on error
- **Error Codes**: 1 for general error
- **Persistence**: Tasks loaded from temporary file; state maintained between command executions

### Complete Command
- **Command**: `todo complete [id]`
- **Input**: Task ID as integer argument
- **Output**: Success message in both human-readable and JSON format
- **Exit Code**: 0 on success, non-zero on error
- **Error Codes**: 1 for general error, 2 for invalid ID, 3 for missing argument
- **Persistence**: Task state updated in temporary file and persists between command executions

### Update Command
- **Command**: `todo update [id] "new content"`
- **Input**: Task ID as integer and new content as string
- **Output**: Success message in both human-readable and JSON format
- **Exit Code**: 0 on success, non-zero on error
- **Error Codes**: 1 for general error, 2 for invalid ID, 3 for missing argument
- **Persistence**: Task state updated in temporary file and persists between command executions

### Delete Command
- **Command**: `todo delete [id]`
- **Input**: Task ID as integer argument
- **Output**: Success message in both human-readable and JSON format
- **Exit Code**: 0 on success, non-zero on error
- **Error Codes**: 1 for general error, 2 for invalid ID, 3 for missing argument
- **Persistence**: Task removed from temporary file and changes persist between command executions