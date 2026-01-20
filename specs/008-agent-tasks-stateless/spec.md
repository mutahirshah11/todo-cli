# Feature Specification: Phase 3.3 Agent-Driven Task Management (Stateless Backend)

**Feature Branch**: `008-agent-tasks-stateless`
**Created**: 2026-01-20
**Status**: Draft
**Input**: User description (Phase 3.3 Spec)

## Clarifications

### Session 2026-01-20
- Q: How is conversation context (e.g., "delete the first one") maintained across stateless requests? → A: Option A: Client sends relevant conversation history in the request payload.
- Q: How should task deletion be handled in the database? → A: Option A: Soft Delete (mark as deleted/set timestamp) to prevent accidental data loss.
- Q: How are MCP tool arguments validated? → A: Option A: Strict Schema (e.g., Pydantic/JSON Schema) to ensure reliable agent input.
- Q: How is user-scoped data access enforced? → A: Option A: System-level restriction where MCP tools automatically filter by `user_id`.
- Q: How does the agent identify a task from natural language? → A: Option A: Natural Language match + Confirmation if confidence is low or match is ambiguous.

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE.
-->

### User Story 1 - Add Task via Agent (Priority: P1)

A user wants to add a new task to their list by describing it to the AI agent, so they can track their work without manual entry.

**Why this priority**: Fundamental capability for a task management system.

**Independent Test**: Can be fully tested by sending a "Create task" prompt and verifying the record exists in Neon DB via a separate verification step.

**Acceptance Scenarios**:

1. **Given** a user prompt "Remind me to buy milk tomorrow", **When** the agent processes the request, **Then** the agent calls the `add_task` MCP tool with correct arguments (title="buy milk", due_date="tomorrow's date") and confirms success to the user.
2. **Given** a stateless backend, **When** the request is processed, **Then** the agent loads necessary context from the DB, executes the tool, and persists the result without relying on in-memory session state.

---

### User Story 2 - Fetch Tasks via Agent (Priority: P1)

A user wants to see their current tasks, so they can know what needs to be done.

**Why this priority**: Core retrieval functionality.

**Independent Test**: Can be tested by seeding the DB with tasks and verifying the agent accurately reports them.

**Acceptance Scenarios**:

1. **Given** a user with 3 tasks in Neon DB, **When** they ask "What do I need to do?", **Then** the agent calls the `list_tasks` MCP tool, retrieves the 3 tasks, and presents them in a natural language summary.
2. **Given** a user with no tasks, **When** they ask "Show my tasks", **Then** the agent calls the tool, receives an empty list, and informs the user gracefully ("You have no tasks pending").

---

### User Story 3 - Update Task via Agent (Priority: P1)

A user wants to modify an existing task (e.g., mark as done, change title), so the list remains accurate.

**Why this priority**: Essential for maintaining data currency.

**Independent Test**: Seed a task, request an update, verify the change in DB.

**Acceptance Scenarios**:

1. **Given** a task "Buy milk", **When** the user says "Change buy milk to buy almond milk", **Then** the agent calls `update_task` with the correct task ID (inferred or retrieved) and the new title.
2. **Given** an ambiguous request like "Update the task", **When** processed, **Then** the agent asks for clarification ("Which task would you like to update?") instead of guessing.

---

### User Story 4 - Remove Task via Agent (Priority: P1)

A user wants to delete a task they no longer need, so their list remains clutter-free.

**Why this priority**: standard CRUD requirement.

**Independent Test**: Seed a task, request deletion, verify it is gone from DB.

**Acceptance Scenarios**:

1. **Given** a task "Call Mom", **When** the user says "Delete the task to call mom", **Then** the agent calls `delete_task` with the correct ID and confirms removal.

---

### Edge Cases

- **Ambiguity**: When user says "Delete it" without context, agent MUST ask "Delete what?" rather than deleting a random task.
- **Invalid Reference**: When user asks to update a non-existent task, agent MUST report "I couldn't find that task" after the tool returns an error/empty result.
- **Tool Failure**: If Neon DB is down or tool fails, agent MUST report "I'm having trouble accessing your tasks right now" rather than crashing or hallucinating success.
- **Statelessness**: A server restart between the user asking "What tasks do I have?" and "Delete the first one" MUST NOT cause the agent to lose context of "the first one" because the client sends the relevant conversation history in the request payload.
- **Context Retention**: The system relies on the client providing conversation history to resolve relative references (e.g., "the first one", "it", "that task"). If history is missing, the agent MUST ask for clarification.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST support `add_task`, `get_tasks`, `update_task`, and `delete_task` operations via MCP tools.
- **FR-002**: All agent operations MUST be scoped to the authenticated user; agent cannot access other users' data.
- **FR-012**: MCP tools MUST automatically enforce user-level isolation by filtering all database queries by the current `user_id`.
- **FR-003**: The backend MUST be stateless; no session state stored in application memory between requests.
- **FR-004**: The agent MUST interact with the database SOLELY through defined MCP tools (no direct SQL generation).
- **FR-011**: All MCP tools MUST enforce strict input validation using schemas (e.g., Pydantic/JSON Schema) to prevent malformed agent requests.
- **FR-005**: The agent MUST infer user intent from natural language and map it to the correct MCP tool and arguments.
- **FR-013**: The agent MUST use natural language matching to identify tasks but MUST ask for confirmation if the match is ambiguous or of low confidence.
- **FR-006**: The agent MUST validate required arguments before calling a tool (e.g., ensure a task title is present for creation).
- **FR-007**: The system MUST persist all successful state changes to Neon DB immediately upon tool execution.
- **FR-010**: Task deletion MUST be implemented as a soft delete (setting `deleted_at`) rather than permanent removal; deleted tasks are excluded from `get_tasks` results by default.
- **FR-008**: The agent MUST handle empty results (e.g., no tasks found) with a user-friendly message, not a raw error code.
- **FR-009**: The agent MUST ask clarifying questions when the user's intent or target (e.g., which task to update) is ambiguous.

### Key Entities

- **Task**: Represents a work item. Attributes: `id` (UUID), `user_id` (Owner), `title` (String), `status` (Pending/Done), `created_at` (Timestamp), `updated_at` (Timestamp), `deleted_at` (Timestamp, Nullable).
- **User**: The owner of the tasks.
- **MCP Tool**: A defined function with a strict input schema exposed to the agent (e.g., `tools.tasks.add`, `tools.tasks.list`).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of successful task creation requests result in a persisted record in Neon DB.
- **SC-002**: Agent successfully maps natural language to correct MCP tool in >95% of standard test cases.
- **SC-003**: System handles server restart in the middle of a conversation flow without user perceiving a state loss (assuming client re-sends history or history is fetched).
- **SC-004**: Zero (0) incidents of the agent attempting direct database access (SQL/REST) outside of MCP tools.
- **SC-005**: Response time for agent task operations (excluding LLM latency) is under 500ms for database persistence.
