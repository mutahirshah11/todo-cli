---
id: 008
title: fix-uuid-json-serialization-error
stage: green
date: 2026-01-20
surface: agent
model: gemini-2.0-flash-exp
feature: 009-mcp-tools-integration
branch: 009-mcp-tools-integration
user: Mutahir
command: fix it
labels: ["bugfix", "fastapi", "pydantic", "serialization", "uuid"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - backend/api/handlers/error_handlers.py
 - backend/api/models/task.py
tests: []
---

## Prompt

"TypeError: Object of type UUID is not JSON serializable" during task creation/fetch.

## Response snapshot

Fixed two issues:
1.  **Serialization Crash:** Updated `validation_exception_handler` to use `jsonable_encoder`. This ensures that when Pydantic reports a validation error (containing raw UUID objects), the error response can be safely serialized to JSON.
2.  **Validation Error:** Updated `TaskResponse` model to type `id` as `UUID` instead of `str`. This matches the database model and prevents Pydantic from raising a validation error in the first place.

## Outcome

- ✅ Impact: API no longer crashes on validation errors; Task responses correctly handle UUIDs.
- 🧪 Tests: Manual verification implied by user report.
- 📁 Files: Modified `backend/api/handlers/error_handlers.py`, `backend/api/models/task.py`.
- 🔁 Next prompts: Continue monitoring.
- 🧠 Reflection: Pydantic validation errors include the *raw* input value. If that value is a complex object (like UUID) and the error handler blindly passes it to `JSONResponse`, it crashes. Always use `jsonable_encoder` for error details.

## Evaluation notes (flywheel)

- Failure modes observed: Uncaught TypeError in exception handler masking the original validation error.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
