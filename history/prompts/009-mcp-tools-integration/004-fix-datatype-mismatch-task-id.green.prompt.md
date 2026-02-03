---
id: 007
title: Fix Datatype Mismatch for Task ID
stage: green
date: 2026-01-20
surface: agent
model: gemini
feature: mcp-tools-integration
branch: 009-mcp-tools-integration
user: Mutahir
command: system-continue
labels: ["fix", "db", "uuid", "sqlmodel"]
links:
  spec: specs/009-mcp-tools-integration/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - backend/api/models/database.py
tests:
 - backend/scripts/verify_task_creation.py
---

## Prompt

System reported DatatypeMismatchError: column "id" is of type uuid but expression is of type character varying.

## Response snapshot

Updated the legacy Task model in backend/api/models/database.py to use uuid.UUID for the id field, matching the updated database schema. Also added missing status and deleted_at fields to keep metadata in sync.

## Outcome

- ✅ Impact: Resolved insert failure due to type mismatch between Python model and Postgres schema.
- 🧪 Tests: Migrations and schema sync verified.
- 📁 Files: Updated backend/api/models/database.py.
- 🔁 Next prompts: /sp.plan Phase 3.4
- 🧠 Reflection: All models (including legacy ones) must be updated when primary key types change.

## Evaluation notes (flywheel)

- Failure modes observed: None.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): v1
- Next experiment (smallest change to try): N/A
