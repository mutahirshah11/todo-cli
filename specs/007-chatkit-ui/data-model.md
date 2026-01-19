# Data Model: Chatbot UI

## Interfaces

### Message
Represents a single message in the chat history.

| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | string | Unique identifier for the message. |
| `role` | 'user' \| 'assistant' | Sender role. |
| `content` | string | Text content (supports markdown). |
| `createdAt` | string | ISO-8601 timestamp. |

### Thread
Represents a collection of messages forming a conversation.

| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | string | Unique thread identifier. |
| `title` | string (optional) | Summary of the conversation. |
| `messages` | Message[] | List of messages in chronilogical order. |

### SessionResponse
Output from the session initialization endpoint.

| Field | Type | Description |
| :--- | :--- | :--- |
| `client_secret` | string | Ephemeral token for ChatKit frontend authentication. |
| `thread_id` | string (optional) | Initial thread ID to load. |
