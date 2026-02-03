---
id: 006
title: fix-auth-users-undefined-table
stage: green
date: 2026-01-20
surface: agent
model: gemini-2.0-flash-exp
feature: 009-mcp-tools-integration
branch: 009-mcp-tools-integration
user: Mutahir
command: fix it
labels: ["bugfix", "database", "alembic", "migration", "auth"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - backend/api/database/models/auth_user.py
 - backend/api/database/models/__init__.py
 - backend/alembic/versions/c3110730b84e_restore_auth_users_table.py
tests:
 - auth/verify_database_schema.py
---

## Prompt

"Login failed due to server error: (psycopg2.errors.UndefinedTable) relation 'auth_users' does not exist"

## Response snapshot

Restored the `auth_users` table by adding the `AuthUser` model to the backend's known models and generating a migration to recreate it. It was previously dropped by an accidental migration.

## Outcome

- ✅ Impact: `auth_users` table created in DB. Login should work.
- 🧪 Tests: `auth/verify_database_schema.py` passed.
- 📁 Files: Added `backend/api/database/models/auth_user.py`, updated `__init__.py`, added migration.
- 🔁 Next prompts: Verify login flow in UI.
- 🧠 Reflection: When splitting services (Auth vs Backend) in a monorepo, ensure the Schema Manager (Backend/Alembic) knows about ALL shared tables, or strictly separate databases. Here, they share the DB, so Backend must define AuthUser.

## Evaluation notes (flywheel)

- Failure modes observed: Missing table in DB despite migration history (due to dropped table in recent migration).
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
