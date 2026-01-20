# Implementation Plan - Phase 3.3: Database & Persistence Layer

**Feature**: Agent-Driven Task Management (Stateless Backend)
**Version**: 1.0
**Status**: Planned

## Technical Context
- **Language**: Python
- **ORM**: SQLModel (Pydantic + SQLAlchemy Core)
- **Database**: Neon Serverless PostgreSQL
- **Framework**: FastAPI (Context)
- **Authentication**: Better Auth (user_id provider)
- **Architecture**: Stateless Backend, Persistent Store

## Constitution Check
- **Article I (TDD)**: All database models and repository methods will be test-driven.
- **Article II (Privacy)**: Strict `user_id` filtering on all queries to ensure isolation.
- **Article IV (Integrity)**: Transactional writes, soft deletes for safety.
- **Article V (Simplicity)**: Normalized schema, minimal abstractions.

## Phase 0: Research & Discovery
- [x] **ORM Selection**: SQLModel confirmed for async support and Pydantic integration.
- [x] **Schema Design**: `Task`, `Conversation`, `Message` entities defined.
- [x] **Persistence Strategy**: Hybrid approach - DB holds truth, Client may provide immediate context.

## Phase 1: Design & Contracts
- [x] **Data Model**: Defined in `data-model.md`.
- [x] **Validation Rules**: Defined strict types and constraints.

## Phase 2: Implementation

### 2.1 Database Configuration & Initialization
**Goal**: Configure SQLModel engine for Neon and setup migration capability.
- **Task**: Verify `DATABASE_URL` in environment.
- **Task**: Configure `create_async_engine` with Neon-specific settings (pool size, etc.).
- **Task**: Ensure Alembic is configured for SQLModel.

### 2.2 Model Implementation
**Goal**: Implement strict SQLModel classes.
- **Task**: Create `backend/api/database/models/task.py` with `deleted_at` support.
- **Task**: Create `backend/api/database/models/conversation.py`.
- **Task**: Create `backend/api/database/models/message.py`.
- **Task**: Verify foreign key relationships and indices.

### 2.3 Persistence Layer (Repositories)
**Goal**: abstract DB access with safe, user-scoped methods.
- **Task**: Create `TaskRepository` with:
  - `create_task(user_id, data)`
  - `get_active_tasks(user_id)` (Filters `deleted_at=None`)
  - `soft_delete_task(user_id, task_id)`
  - `update_task(user_id, task_id, data)`
- **Task**: Create `ConversationRepository` with:
  - `create_conversation(user_id)`
  - `add_message(conversation_id, role, content)`
  - `get_history(conversation_id, limit)`
- **Constraint**: Every method must require `user_id` and validate ownership.

### 2.4 Migrations
**Goal**: Apply schema to Neon.
- **Task**: Generate Alembic migration script (`migrations/versions/xxxx_add_task_agent_tables.py`).
- **Task**: Apply migration to dev environment.

### 2.5 Testing (TDD)
**Goal**: Verify integrity and constraints.
- **Task**: `tests/unit/test_models.py`: Verify validation and constraints.
- **Task**: `tests/integration/test_persistence.py`:
  - Verify `user_id` isolation (User A cannot see User B's tasks).
  - Verify Soft Delete logic.
  - Verify Conversation history retrieval.

## Dependencies & Handover
- **Phase 3.4 (MCP Tools)**: Will import `TaskRepository` to implement tool logic.
- **Phase 3.1 (Agents)**: Will rely on `Message` table structure for context loading.
- **Phase 3.2 (UI)**: Will query `Task` table for dashboard display.