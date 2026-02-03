# Tasks: MCP Tools Integration

**Branch**: `009-mcp-tools-integration`
**Status**: Pending

## Dependencies

- [ ] Phase 1 (Setup) -> Phase 2 (Foundation)
- [ ] Phase 2 (Foundation) -> Phase 3 (Create Task)
- [ ] Phase 3 (Create Task) -> Phase 4 (List Tasks)
- [ ] Phase 3 (Create Task) -> Phase 5 (Modify/Manage Tasks)

## Phase 1: Setup

**Goal**: Initialize the MCP tools environment and structure.

- [x] T001 Install `mcp` SDK and update `requirements.txt`
- [x] T002 Create MCP server entry point structure in `backend/mcp_server.py`
- [x] T003 Create MCP tools module structure in `backend/api/mcp/__init__.py`, `backend/api/mcp/tools.py`, and `backend/api/mcp/utils.py`
- [x] T004 Create test directory structure in `backend/tests/mcp/unit` and `backend/tests/mcp/integration`
- [x] T005 Create empty `backend/tests/mcp/conftest.py` for MCP-specific fixtures

## Phase 2: Foundation

**Goal**: Establish the stateless MCP server shell and database integration pattern.

- [x] T006 [P] Implement `utils.py` for standardized error formatting and JSON response helpers in `backend/api/mcp/utils.py`
- [x] T007 Implement database session context manager wrapper for MCP tools in `backend/api/mcp/utils.py` (reusing `AsyncSessionLocal`)
- [x] T008 Create unit test for MCP server initialization and transport in `backend/tests/mcp/unit/test_server_init.py`
- [x] T009 Implement basic MCP server setup with Stdio transport in `backend/mcp_server.py`

## Phase 3: User Story 1 - Create Task

**Goal**: Enable AI Agents to create tasks via `add_task`.

**Independent Test**: Call `add_task` with `user_id` and `title`, verify task appears in DB.

- [x] T010 [US1] Create unit test for `add_task` tool logic (mocking DB) in `backend/tests/mcp/unit/test_tool_add_task.py`
- [x] T011 [US1] Implement `add_task` tool definition and logic in `backend/api/mcp/tools.py`
- [x] T012 [US1] Register `add_task` tool in `backend/mcp_server.py`
- [x] T013 [US1] Create integration test for `add_task` (using real DB) in `backend/tests/mcp/integration/test_add_task_integration.py`
- [x] T014 [US1] Verify `add_task` handles validation errors (missing title, invalid user_id) correctly

## Phase 4: User Story 2 - List User Tasks

**Goal**: Enable AI Agents to retrieve tasks via `list_tasks`.

**Independent Test**: Seed tasks, call `list_tasks`, verify output matches.

- [x] T015 [US2] Create unit test for `list_tasks` tool logic (mocking DB) in `backend/tests/mcp/unit/test_tool_list_tasks.py`
- [x] T016 [US2] Implement `list_tasks` tool definition and logic in `backend/api/mcp/tools.py`
- [x] T017 [US2] Register `list_tasks` tool in `backend/mcp_server.py`
- [x] T018 [US2] Create integration test for `list_tasks` in `backend/tests/mcp/integration/test_list_tasks_integration.py`
- [x] T019 [US2] Verify `list_tasks` filters by status and handles empty results

## Phase 5: User Story 3 - Modify/Manage Tasks

**Goal**: Enable AI Agents to update, complete, and delete tasks.

**Independent Test**: Create task, update/complete/delete it, verify state changes.

- [x] T020 [US3] Create unit tests for `update_task`, `complete_task`, `delete_task` in `backend/tests/mcp/unit/test_tool_manage_tasks.py`
- [x] T021 [US3] Implement `update_task` tool definition and logic in `backend/api/mcp/tools.py`
- [x] T022 [US3] Implement `complete_task` tool definition and logic in `backend/api/mcp/tools.py`
- [x] T023 [US3] Implement `delete_task` tool definition and logic in `backend/api/mcp/tools.py`
- [x] T024 [US3] Register `update_task`, `complete_task`, `delete_task` in `backend/mcp_server.py`
- [x] T025 [US3] Create integration tests for management tools in `backend/tests/mcp/integration/test_manage_tasks_integration.py`
- [x] T026 [US3] Verify ownership validation (User A cannot modify User B's task)

## Phase 6: Polish

**Goal**: Finalize documentation and verify end-to-end functionality.

- [x] T027 [P] Update `README.md` with MCP server running instructions
- [x] T028 Run full test suite (`pytest backend/tests/mcp`) and ensure 100% pass rate
- [x] T029 Perform manual end-to-end test using `mcp-inspector` (if available) or script

## Implementation Strategy

1.  **MVP Scope**: Phases 1, 2, and 3 (Create Task) allow the agent to start writing data.
2.  **Incremental Delivery**: Add read capabilities (Phase 4) and then full management (Phase 5).
3.  **Testing**: Strict TDD. Write the test file first, run it (fail), then implement.
