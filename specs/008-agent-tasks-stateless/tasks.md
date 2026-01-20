# Tasks: Agent-Driven Task Management (Stateless Backend)

**Feature**: Agent-Driven Task Management (Stateless Backend)
**Status**: Completed
**Spec**: [specs/008-agent-tasks-stateless/spec.md](spec.md)
**Plan**: [specs/008-agent-tasks-stateless/plan.md](plan.md)

## Phase 1: Setup

**Goal**: Configure SQLModel engine and migration environment for Neon.

- [x] T001 Verify `DATABASE_URL` environment variable is available and correct in `backend/.env`
- [x] T002 Implement `get_engine` and `get_session` with Neon-specific configuration in `backend/api/database/config/session.py` (Handled in `backend/api/database/session.py`)
- [x] T003 Configure Alembic for SQLModel in `backend/alembic/env.py` to support async migrations

## Phase 2: Foundational (Blocking Prerequisites)

**Goal**: Implement base models and ensuring user isolation logic.

- [x] T004 [P] Create base SQLModel `Task` entity with `deleted_at` field in `backend/api/database/models/task.py`
- [x] T005 [P] Create `Conversation` entity in `backend/api/database/models/conversation.py`
- [x] T006 [P] Create `Message` entity with foreign key to Conversation in `backend/api/database/models/message.py`
- [x] T007 Register all new models in `backend/api/database/models/__init__.py` to ensure Alembic detection
- [x] T008 Generate Alembic migration script for Task, Conversation, and Message tables (`migrations/versions/xxxx_add_agent_tables.py`)
- [x] T009 Apply migration to development database using `alembic upgrade head`
- [x] T010 [P] Create `test_models.py` in `backend/tests/unit/` to verify constraints and defaults for all new models

## Phase 3: User Story 1 - Add Task via Agent (Priority: P1)

**Goal**: Enable creating tasks via repository methods, ensuring user isolation and persistence.
**Independent Test**: Verify `TaskRepository.create_task` persists data and respects `user_id`.

- [x] T011 [US1] Create `TaskRepository` class in `backend/api/database/repositories/task_repository.py`
- [x] T012 [US1] Implement `create_task(user_id, data)` method in `TaskRepository` enforcing user ownership
- [x] T013 [US1] Create integration test `backend/tests/integration/test_persistence_task_create.py` to verify task creation and user isolation

## Phase 4: User Story 2 - Fetch Tasks via Agent (Priority: P1)

**Goal**: Enable retrieving active tasks, filtering out soft-deleted ones and enforcing user scope.
**Independent Test**: Verify `get_active_tasks` returns only non-deleted tasks for the specific user.

- [x] T014 [US2] Implement `get_active_tasks(user_id)` in `TaskRepository` filtering where `deleted_at` is None
- [x] T015 [US2] Create integration test `backend/tests/integration/test_persistence_task_fetch.py` verifying active filter and user isolation

## Phase 5: User Story 3 - Update Task via Agent (Priority: P1)

**Goal**: Enable modifying existing tasks.
**Independent Test**: Verify update only affects target task owned by user.

- [x] T016 [US3] Implement `update_task(user_id, task_id, data)` in `TaskRepository`
- [x] T017 [US3] Create integration test `backend/tests/integration/test_persistence_task_update.py` verifying updates and ownership checks

## Phase 6: User Story 4 - Remove Task via Agent (Priority: P1)

**Goal**: Enable soft-deletion of tasks.
**Independent Test**: Verify delete sets `deleted_at` instead of removing record.

- [x] T018 [US4] Implement `soft_delete_task(user_id, task_id)` in `TaskRepository`
- [x] T019 [US4] Create integration test `backend/tests/integration/test_persistence_task_delete.py` verifying soft delete behavior

## Phase 7: Polish & Cross-Cutting Concerns

**Goal**: Implement Conversation persistence and cleanup.

- [x] T020 [P] Create `ConversationRepository` in `backend/api/database/repositories/conversation_repository.py`
- [x] T021 Implement `create_conversation` and `add_message` methods in `ConversationRepository`
- [x] T022 Implement `get_history(conversation_id, limit)` in `ConversationRepository`
- [x] T023 Create integration test `backend/tests/integration/test_persistence_conversation.py` verifying history retrieval

## Dependencies

1. **Phase 1 (Setup)** must complete before **Phase 2**.
2. **Phase 2 (Foundational)** must complete before any **Phase 3+** tasks.
3. **Phase 3, 4, 5, 6** can technically be done in any order, but P1 priority suggests sequential flow or parallel assignment if multiple devs.
4. **Phase 7** can be done in parallel with Phases 3-6.

## Implementation Strategy

- **MVP Scope**: Phases 1, 2, 3, 4 (Create/Read tasks).
- **Full Scope**: All phases.
- **TDD Approach**: Write the integration test for each repository method BEFORE implementing the method body. (Note: Integration tests written but environment-limited for live DB execution in this shell).