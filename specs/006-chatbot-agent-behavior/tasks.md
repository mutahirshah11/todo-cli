# Tasks: Chatbot Agent Behavior (Phase 3.1)

**Feature**: Chatbot Agent Behavior
**Status**: Pending
**Priority**: High
**Guideline**: Use OpenAI Agents SDK / Context7 official syntax. Avoid custom class boilerplate where SDK provides abstractions.

## Phase 1: Setup & Research
- [x] T001 Research OpenAI Agents SDK and Context7 official syntax for defining agents and tools. Document findings in `specs/006-chatbot-agent-behavior/research.md`.
- [x] T002 Initialize `backend/api/agent/` directory and create `__init__.py`.
- [x] T003 Install required dependencies (`openai`, `pydantic`) and update `backend/requirements.txt`.
- [x] T004 Define Data Models (`AgentRequest`, `AgentResponse`, `Message`) in `backend/api/agent/models.py` using Pydantic.

## Phase 2: Foundational (Blocking)
- [x] T005 Define Tool Interfaces (Schemas) for `add_task`, `list_tasks`, `update_task`, `delete_task`, `complete_task` in `backend/api/agent/tools.py` using SDK standard syntax.
- [x] T006 Create Mock MCP Tool implementations in `backend/tests/agent/mock_tools.py` for independent testing.
- [x] T007 Setup Test Suite infrastructure in `backend/tests/agent/conftest.py` including `AsyncOpenAI` client mocks.

## Phase 3: User Story 1 - Add Task (P1)
**Goal**: Enable users to create tasks via natural language.
- [x] T008 [US1] Create test cases for "Add Task" intent (simple and with parameters) in `backend/tests/agent/test_add_task.py`.
- [x] T009 [US1] Implement "Add Task" agent logic in `backend/api/agent/core.py` using OpenAI Agents SDK, wiring it to `add_task` tool.
- [x] T010 [US1] Implement parameter extraction logic (handling explicit vs implicit dates) in `backend/api/agent/core.py`.
- [x] T011 [US1] Verify "Add Task" flow with tests.

## Phase 4: User Story 2 - List Tasks (P1)
**Goal**: Enable users to view tasks with optional filters.
- [x] T012 [P] [US2] Create test cases for "List Tasks" intent (all, completed, pending) in `backend/tests/agent/test_list_tasks.py`.
- [x] T013 [US2] Register `list_tasks` tool with the agent in `backend/api/agent/core.py` and implement routing logic.
- [x] T014 [US2] Verify "List Tasks" flow with tests.

## Phase 5: User Story 3 - Update/Complete with Context (P2)
**Goal**: Modify tasks using context (pronouns, history).
- [x] T015 [US3] Create test cases for Context Resolution (e.g., "Delete it" after listing) in `backend/tests/agent/test_context.py`.
- [x] T016 [US3] Implement Context Management logic in `backend/api/agent/core.py` to pass conversation history to the SDK/Model.
- [x] T017 [US3] Register `update_task` and `complete_task` tools in `backend/api/agent/core.py`.
- [x] T018 [US3] Verify Context Resolution and Update flows with tests.

## Phase 6: User Story 4 - Delete Task (P3)
**Goal**: Remove tasks.
- [x] T019 [P] [US4] Create test cases for "Delete Task" intent in `backend/tests/agent/test_delete_task.py`.
- [x] T020 [US4] Register `delete_task` tool in `backend/api/agent/core.py`.
- [x] T021 [US4] Implement ambiguity handling (asking for ID if unclear) in `backend/api/agent/core.py`.
- [x] T022 [US4] Verify Delete flow with tests.

## Phase 7: Polish & Integration
- [x] T023 Implement global Error Handling (unknown tools, API failures) in `backend/api/agent/core.py`.
- [x] T024 [P] Refactor `backend/api/agent/core.py` to ensure strict adherence to "Context7/OpenAI Agents SDK" official syntax (clean up any custom boilerplate).
- [x] T025 Run full regression suite `pytest backend/tests/agent/`.

## Dependencies
1. US1 & US2 are independent.
2. US3 depends on US1 & US2 (needs tasks to update/list).
3. US4 is independent but best done after US3.

## Implementation Strategy
- **MVP**: US1 (Add) + US2 (List).
- **Iteration**: US3 (Context) is the complex part; implement carefully.
- **Strict Adherence**: Ensure every step uses the official SDK patterns as requested.