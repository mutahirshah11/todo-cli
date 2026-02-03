# Data Model: MCP Tools Integration

## Entities

### Task (Existing)
*Source: `backend/api/models/task.py`*

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | UUID | Yes | Unique identifier (PK) |
| `title` | String | Yes | Task title (1-100 chars) |
| `description` | String | No | Task details (max 500 chars) |
| `completed` | Boolean | Yes | Completion status |
| `user_id` | String | Yes | Owner identifier |
| `created_at` | DateTime | Yes | Timestamp |
| `updated_at` | DateTime | Yes | Timestamp |

## MCP Tool Schemas

The following schemas define the inputs for the exposed tools.

### `add_task`
```json
{
  "name": "add_task",
  "description": "Create a new task for a user",
  "inputSchema": {
    "type": "object",
    "properties": {
      "user_id": { "type": "string", "description": "The ID of the user owning the task" },
      "title": { "type": "string", "description": "The title of the task" },
      "description": { "type": "string", "description": "Optional description of the task" }
    },
    "required": ["user_id", "title"]
  }
}
```

### `list_tasks`
```json
{
  "name": "list_tasks",
  "description": "List tasks for a user with optional filtering",
  "inputSchema": {
    "type": "object",
    "properties": {
      "user_id": { "type": "string", "description": "The ID of the user" },
      "status": { "type": "string", "enum": ["pending", "completed"], "description": "Filter by task status" },
      "include_deleted": { "type": "boolean", "description": "Whether to include soft-deleted tasks" }
    },
    "required": ["user_id"]
  }
}
```

### `update_task`
```json
{
  "name": "update_task",
  "description": "Update an existing task",
  "inputSchema": {
    "type": "object",
    "properties": {
      "user_id": { "type": "string", "description": "The ID of the user" },
      "task_id": { "type": "string", "description": "The UUID of the task to update" },
      "title": { "type": "string", "description": "New title" },
      "description": { "type": "string", "description": "New description" }
    },
    "required": ["user_id", "task_id"]
  }
}
```

### `complete_task`
```json
{
  "name": "complete_task",
  "description": "Mark a task as completed",
  "inputSchema": {
    "type": "object",
    "properties": {
      "user_id": { "type": "string", "description": "The ID of the user" },
      "task_id": { "type": "string", "description": "The UUID of the task to complete" }
    },
    "required": ["user_id", "task_id"]
  }
}
```

### `delete_task`
```json
{
  "name": "delete_task",
  "description": "Delete (soft-delete) a task",
  "inputSchema": {
    "type": "object",
    "properties": {
      "user_id": { "type": "string", "description": "The ID of the user" },
      "task_id": { "type": "string", "description": "The UUID of the task to delete" }
    },
    "required": ["user_id", "task_id"]
  }
}
```
