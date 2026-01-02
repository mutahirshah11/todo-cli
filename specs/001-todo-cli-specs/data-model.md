# Data Model: Todo CLI Application

## Task Entity

**Name**: Task
**Description**: Represents a single todo item with unique identifier, content, and completion status

### Fields
- **id**: integer (required) - Unique sequential identifier for the task
- **content**: string (required) - The task description/content
- **completed**: boolean (required, default: false) - Completion status of the task

### Validation Rules
- id: Must be a positive integer
- content: Must not be empty or null
- completed: Must be a boolean value

### State Transitions
- Initially: completed = false
- After 'complete' operation: completed = true
- After 'incomplete' operation (if implemented): completed = false

## TaskList Collection

**Name**: TaskList
**Description**: In-memory collection of Task entities with temporary file persistence, managed during application execution

### Operations
- **add_task(content: string)**: Creates new Task with next sequential ID and adds to collection, persists to temporary file
- **get_all_tasks()**: Loads tasks from temporary file, returns all tasks in collection
- **get_task_by_id(id: integer)**: Loads tasks from temporary file, returns specific task by ID or null if not found
- **update_task(id: integer, content: string)**: Updates content of existing task, persists to temporary file
- **delete_task(id: integer)**: Removes task from collection, persists to temporary file
- **mark_complete(id: integer)**: Updates completion status to true, persists to temporary file
- **mark_incomplete(id: integer)**: Updates completion status to false (if applicable), persists to temporary file

### Constraints
- Task IDs must be unique within the collection
- Task IDs must be sequential starting from 1
- Task content must not be empty
- State must be persisted to temporary file after each operation