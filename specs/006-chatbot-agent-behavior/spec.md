# Feature Specification: Chatbot Agent Behavior (Phase 3.1)

**Feature Branch**: `006-chatbot-agent-behavior`
**Created**: 2026-01-18
**Status**: Draft
**Input**: Phase 3.1 AI agent behavior using OpenAI Agents SDK.

## Clarifications

### Session 2026-01-18
- Q: How should temporal references like "tomorrow" in "Call mom tomorrow" be handled? → A: Extract to `due_date` (ISO-8601).
- Q: What format should MCP tools use for returning data to the AI agent? → A: Strict JSON Schema (Agent formats the text response).
- Q: How should the agent handle missing required information like a task title? → A: Support multi-step (Ask the user for the missing details sequentially).

## Overview

Phase 3 transforms the Tickwen task manager into an **AI-powered chatbot** where users can manage tasks using natural language. This specific spec (Phase 3.1) defines **exactly how the AI agent should interpret user commands, map them to MCP tools, handle conversation context, and respond to users**.

The AI agent acts as a stateless interpreter that:
1.  Receives natural language input from the user (along with conversation history).
2.  Determines the user's intent (Add, List, Update, Complete, Delete).
3.  Maps this intent to specific **MCP Tools** (`add_task`, `list_tasks`, `complete_task`, `delete_task`, `update_task`).
4.  Executes the tool via the MCP server integration.
5.  Returns a friendly, context-aware response to the user by formatting the tool's JSON output.

**Crucial Constraints:**
*   All task operations MUST go through MCP tools. The agent cannot modify the database directly.
*   The server is **stateless**. Conversation context must be provided with each request (fetched from DB).
*   **Tool Outputs**: All MCP tools MUST return data in a strict JSON format. The AI Agent is responsible for generating the natural language response based on this data.
*   **Conversational Flow**: The agent MUST support multi-turn interactions to collect missing required parameters (e.g., asking for a title if only "Add task" is provided).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Add Task (Priority: P1)

Users should be able to create new tasks using natural language, specifying details like title and description implicitly or explicitly.

**Why this priority**: Core functionality of a todo app.

**Independent Test**: Can be tested by sending various "add" phrasings and verifying `add_task` tool invocation.

**Acceptance Scenarios**:

1.  **Given** user says "Buy groceries", **When** processed, **Then** agent calls `add_task(title="Buy groceries")` and responds confirming addition.
2.  **Given** user says "Remind me to call mom tomorrow", **When** processed, **Then** agent extracts "tomorrow" to an ISO-8601 `due_date`, calls `add_task(title="Call mom", due_date="2026-01-19T...")` and confirms.
3.  **Given** user says "Add task", **When** processed, **Then** agent asks "What should I name the task?" and waits for the user's next response to complete the `add_task` call.

### User Story 2 - List Tasks (Priority: P1)

Users should be able to view their tasks, potentially filtering by status.

**Why this priority**: Users need to see what they have to do.

**Independent Test**: Send "Show tasks", "List done tasks" and verify `list_tasks` tool invocation with correct status filters.

**Acceptance Scenarios**:

1.  **Given** user says "Show me my tasks", **When** processed, **Then** agent calls `list_tasks(status=null/all)` and presents the list.
2.  **Given** user says "What have I finished?", **When** processed, **Then** agent calls `list_tasks(status="completed")` and shows completed tasks.
3.  **Given** user says "What is pending?", **When** processed, **Then** agent calls `list_tasks(status="pending")`.

### User Story 3 - Update/Complete Task with Context (Priority: P2)

Users should be able to modify tasks, often referring to them by vague references ("it", "that one") after listing them.

**Why this priority**: Natural conversation flow requires context awareness.

**Independent Test**: Perform a sequence: List -> Update "it". Verify agent identifies the correct task ID from history.

**Acceptance Scenarios**:

1.  **Given** previous turn showed Task 5 ("Buy Milk"), **When** user says "Mark it as done", **Then** agent calls `complete_task(task_id=5)` and confirms.
2.  **Given** previous turn showed Task 3 ("Walk dog"), **When** user says "Change that to Walk dog in park", **Then** agent calls `update_task(task_id=3, title="Walk dog in park")`.
3.  **Given** no context, **When** user says "Delete it", **Then** agent asks "Which task would you like to delete?" (Error handling).

### User Story 4 - Delete Task (Priority: P3)

Users should be able to remove tasks.

**Why this priority**: Standard CRUD operation.

**Independent Test**: Send "Delete task X" and verify `delete_task` call.

**Acceptance Scenarios**:

1.  **Given** user says "Delete task 4", **When** processed, **Then** agent calls `delete_task(task_id=4)` and confirms.
2.  **Given** user says "Remove the meeting task", **When** processed, **Then** agent searches/identifies "meeting task" (likely via search tool or list+filter logic) and deletes it (or asks for confirmation if ambiguous). *MVP: Require ID or clear name match.*

### Edge Cases

- **Ambiguous Requests**: What happens when user says "Delete the task" but has 5 tasks?
  - *Behavior*: Agent MUST ask "Which task would you like to delete? Please provide the ID or name."
- **Unknown Tool**: What happens when user asks "What is the weather?" (unsupported intent)?
  - *Behavior*: Agent MUST respond "I can only help you manage your tasks. I don't have access to weather information."
- **Missing Parameters**: What happens when user says "Add task" with no title?
  - *Behavior*: Agent MUST ask "What should I name the task?"

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001 (Intent Mapping)**: The system MUST map natural language inputs to the following MCP tools:
    - "Add...", "Remind me..." -> `add_task`
    - "List...", "Show...", "What's..." -> `list_tasks`
    - "Mark... done", "Finish..." -> `complete_task`
    - "Change...", "Rename..." -> `update_task`
    - "Delete...", "Remove..." -> `delete_task`
- **FR-002 (Parameter Extraction)**: The system MUST extract required parameters for tools:
    - `add_task`: title, description (optional), `due_date` (optional, ISO-8601).
    - `update_task`: task_id, title/description/status/due_date (as needed).
    - `complete_task`: task_id.
    - `delete_task`: task_id.
- **FR-003 (Context Awareness)**: The system MUST utilize conversation history to resolve pronouns ("it", "that", "the task") to specific `task_id`s referenced in immediate previous turns.
- **FR-004 (Statelessness)**: The agent MUST accept conversation history and `user_id` as input for every request; it must not rely on internal memory between requests.
- **FR-005 (Feedback)**: The system MUST provide professional, friendly text responses confirming the action taken (e.g., "Task 'X' updated.") or explaining errors (e.g., "I couldn't find that task.").
- **FR-006 (Error Handling)**: If a tool call fails (e.g., Task ID not found), the agent MUST relay this clearly to the user, asking for clarification.
- **FR-007 (JSON Processing)**: The system MUST process strict JSON responses from MCP tools and translate them into natural language for the user.
- **FR-008 (Parameter Collection)**: If a mandatory parameter (like task title) is missing, the agent MUST prompt the user for it rather than failing.

### Key Entities

- **User Intent**: The derived goal of the user (e.g., CREATE_TASK, QUERY_TASKS).
- **Conversation Context**: The sliding window of recent messages (User + AI) used to resolve references.
- **MCP Tool Definition**: The strict schema (JSON) required to invoke backend functions.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Agent correctly identifies user intent (Add/List/Update/Delete) for >95% of standard phrasing variations (as defined in test cases).
- **SC-002**: Agent correctly extracts parameters (Task IDs, titles) for >90% of requests.
- **SC-003**: Agent successfully resolves context-dependent references ("delete it") in >90% of valid multi-turn sequences (List -> Action).
- **SC-004**: All state-changing actions (Add/Update/Delete) result in a confirmation message to the user.

## Future Integration Notes

- **Phase 3.2 (Frontend)**: Will consume the text response from this agent.
- **Phase 3.3 (Database)**: Will store the messages generated here.
- **Phase 3.4 (MCP)**: This agent will call the actual tools implemented in Phase 3.4. For 3.1, tools can be mocked or stubs.

## Mapping Intents to MCP Tools (Reference)

| User Intent | MCP Tool | Parameters | Output |
|:---|:---|:---|:---|
| Add Task | `add_task` | `user_id`, `title`, `description` (opt), `due_date` (opt) | Task object (JSON) |
| List Tasks | `list_tasks` | `user_id`, `status` (opt: "pending", "completed") | List of Task objects (JSON) |
| Complete Task | `complete_task` | `task_id` | Updated Task object (JSON) |
| Update Task | `update_task` | `task_id`, `title` (opt), `description` (opt), `due_date` (opt) | Updated Task object (JSON) |
| Delete Task | `delete_task` | `task_id` | Success/Error object (JSON) |

## Examples

**1. Adding a Task**
> User: "Add task to buy groceries"
> AI: (Calls `add_task(title="Buy groceries")`) -> Success
> AI Response: "I've added 'Buy groceries' to your list."

**2. Contextual Completion**
> User: "Show my tasks"
> AI: (Calls `list_tasks()`) -> Returns [Task 1: Gym, Task 2: Work]
> AI Response: "Here are your tasks: 1. Gym, 2. Work"
> User: "I finished the first one"
> AI: (Resolves "first one" -> ID 1) -> Calls `complete_task(task_id=1)`
> AI Response: "Great job! I've marked 'Gym' as completed."
