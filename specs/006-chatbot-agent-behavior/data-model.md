# Data Model - Phase 3.1

## Entities

### AgentRequest
Represents a single stateless interaction request to the agent.

| Field | Type | Description |
| :--- | :--- | :--- |
| `user_id` | String | Unique identifier for the user. |
| `message` | String | The current natural language input from the user. |
| `history` | List[Message] | Previous conversation turns (User + Assistant). |

### Message
Represents a single turn in the conversation history.

| Field | Type | Description |
| :--- | :--- | :--- |
| `role` | Enum | `user`, `assistant`, `system`. |
| `content` | String | Text content of the message. |
| `tool_calls` | List[ToolCall] | (Optional) List of tool calls made by the assistant. |

### ToolCall
Represents a specific invocation of an MCP tool.

| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | String | Unique ID for the tool call (required for matching outputs). |
| `type` | String | Always `function`. |
| `function` | Object | Contains `name` and `arguments` (JSON string). |

### AgentResponse
The final output from the agent after processing.

| Field | Type | Description |
| :--- | :--- | :--- |
| `content` | String | The natural language response to the user. |
| `tool_calls` | List[ToolCall] | (Optional) Tools invoked during processing. |
