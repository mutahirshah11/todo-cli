# Research: Database & Persistence Layer (Phase 3.3)

**Feature**: Agent-Driven Task Management (Stateless Backend)
**Date**: 2026-01-20

## Decisions & Rationale

### 1. ORM: SQLModel
- **Decision**: Use SQLModel.
- **Rationale**: Combines Pydantic validation with SQLAlchemy's ORM capabilities, perfect for FastAPI. Native async support.
- **Alternatives**: SQLAlchemy (too verbose), Tortoise-ORM (less Pydantic integration).

### 2. Conversation Persistence vs. Statelessness
- **Decision**: Persist full conversation history in DB (`Conversation` + `Message` tables), but allow client to pass context in payload if needed for immediate stateless resolution.
- **Rationale**: The Plan prompt strictly requires "All state (tasks, conversations, messages) must be persisted". While the Spec clarification mentions client-side history for "stateless context", persisting history in the DB is critical for:
    1.  Audit logs.
    2.  Multi-device synchronization (user switches devices).
    3.  Future analysis.
- **Implementation**: API will likely accept a `conversation_id`. If provided, it can load history from DB (or validate client payload against it). For the "Database Phase", we simply provide the tables and CRUD.

### 3. Soft Deletes for Tasks
- **Decision**: Use `deleted_at` (Timestamp, nullable).
- **Rationale**: Spec Requirement FR-010. Allows recovery and auditing.

### 4. User Isolation
- **Decision**: All queries must filter by `user_id` at the repository/service level.
- **Rationale**: Constitution Article II (Privacy).

## Unknowns Resolved
- **Message Schema**: Standardized to `role` (enum: user, assistant, system), `content` (text), `timestamp`.
- **Indexes**: Index `user_id` on all tables for performance. Index `deleted_at` on Tasks for filtering.
