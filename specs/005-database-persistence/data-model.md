# Data Model: Database Integration for Todo Full-Stack Web Application

## Entity Definitions

### User Entity
- **Entity Name**: User
- **Fields**:
  - `user_id`: UUID (Primary Key) - Unique identifier for the user (from JWT token)
  - `email`: String (255) - User's email address (indexed, unique)
  - `created_at`: DateTime - Timestamp of account creation
  - `updated_at`: DateTime - Timestamp of last update
  - `is_active`: Boolean - Whether the account is active

- **Constraints**:
  - `user_id` must be unique and non-null
  - `email` must be unique and valid format
  - `created_at` auto-populates on creation
  - `updated_at` auto-updates on modification

### Task Entity
- **Entity Name**: Task
- **Fields**:
  - `id`: UUID (Primary Key) - Unique identifier for the task
  - `title`: String (255) - Task title (required)
  - `description`: Text (optional) - Task description
  - `is_completed`: Boolean - Completion status (default: false)
  - `user_id`: UUID (Foreign Key) - Reference to owning user
  - `created_at`: DateTime - Timestamp of task creation
  - `updated_at`: DateTime - Timestamp of last update

- **Constraints**:
  - `id` must be unique and non-null
  - `title` must be non-null and max 255 characters
  - `user_id` must reference an existing User
  - `created_at` auto-populates on creation
  - `updated_at` auto-updates on modification

## Relationships

### User to Task (One-to-Many)
- **Relationship Type**: One User to Many Tasks
- **Constraint**: Foreign Key from Task.user_id to User.user_id
- **Cascade Rule**: Prevent cascade delete to maintain data integrity
- **Access Pattern**: User.tasks (collection of associated tasks)

## Validation Rules

### Task Validation
- Title: Required, minimum 1 character, maximum 255 characters
- Description: Optional, maximum 1000 characters
- Completion status: Boolean value only (true/false)
- User ownership: Must match authenticated user's ID from JWT

### User Validation
- Email: Required, valid email format, unique across all users
- User ID: Must be a valid UUID format from JWT token
- Active status: Boolean indicating account validity

## Indexes

### Required Indexes
- User.email: Unique index for fast email lookups
- Task.user_id: Index for efficient user-task filtering
- Task.created_at: Index for chronological sorting
- Task.is_completed: Index for filtering by completion status

## State Transitions

### Task State Transitions
```
Pending → Completed (when marked complete)
Completed → Pending (when marked incomplete)
```

### User State Transitions
```
Inactive → Active (when account is activated)
Active → Inactive (when account is deactivated)
```

## Data Integrity Rules

### Referential Integrity
- Task.user_id must reference an existing User.user_id
- No orphaned tasks allowed in the system
- User deletion should be handled with care to maintain data integrity

### Access Control
- Each task must have exactly one owner (user_id)
- Users can only access tasks where user_id matches their own ID
- Unauthorized access attempts should return 404 or 403 responses