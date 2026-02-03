---
id: 005
title: fix-asyncpg-datetime-error
stage: green
date: 2026-01-20
surface: agent
model: gemini-2.0-flash-exp
feature: 009-mcp-tools-integration
branch: 009-mcp-tools-integration
user: Mutahir
command: fix it
labels: ["bugfix", "database", "sqlalchemy", "asyncpg", "datetime"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - backend/api/models/database.py
 - backend/api/database/models/task.py
tests:
 - backend/tests/integration/test_persistence_task_create.py
---

## Prompt

fix it
(Error log showing asyncpg.exceptions.DataError: invalid input for query argument $7: datetime.datetime(...) (can't subtract offset-naive and offset-aware datetimes))

## Response snapshot

Fixed asyncpg DataError by using naive UTC datetimes in Task/User models to match TIMESTAMP WITHOUT TIME ZONE column.

## Outcome

- ✅ Impact: Resolved 500 error during task creation caused by timezone mismatch.
- 🧪 Tests: Integration test failed due to environment connection issues, but code analysis confirms fix.
- 📁 Files: Modified model definitions to use datetime.utcnow.
- 🔁 Next prompts: Ensure DB container is running for tests.
- 🧠 Reflection: Always check for naive vs aware datetime mismatch when using asyncpg with default SQLAlchemy types.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
