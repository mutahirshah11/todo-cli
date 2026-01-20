# Data Model: Phase 3.3

## Entities

### 1. Task
Represents a user's todo item.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | UUID | Yes | Primary Key. Defaults to `uuid4`. |
| `user_id` | String | Yes | Owner ID (from Auth). Indexed. |
| `title` | String | Yes | Task description. |
| `status` | Enum | Yes | `pending`, `completed`. Default: `pending`. |
| `created_at` | DateTime | Yes | UTC timestamp. |
| `updated_at` | DateTime | Yes | UTC timestamp. |
| `deleted_at` | DateTime | No | Nullable. If present, task is soft-deleted. |

**Indexes**:
- `(user_id, status)`: For fetching active tasks.
- `(user_id, deleted_at)`: For including/excluding deleted items.

### 2. Conversation
Represents a chat session.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | UUID | Yes | Primary Key. |
| `user_id` | String | Yes | Owner ID. Indexed. |
| `title` | String | No | Auto-generated summary (optional). |
| `created_at` | DateTime | Yes | UTC timestamp. |
| `updated_at` | DateTime | Yes | UTC timestamp. |

### 3. Message
Represents a single turn in a conversation.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | UUID | Yes | Primary Key. |
| `conversation_id` | UUID | Yes | Foreign Key to Conversation. Indexed. |
| `role` | Enum | Yes | `user`, `assistant`, `system`. |
| `content` | Text | Yes | The message body. |
| `created_at` | DateTime | Yes | UTC timestamp. |

## Relationships
- **User** (Logical) has many **Tasks**.
- **User** (Logical) has many **Conversations**.
- **Conversation** has many **Messages**.

## Validation Rules
- `title`: Min length 1.
- `role`: Must be one of valid enum values.
- `user_id`: Must not be empty.
