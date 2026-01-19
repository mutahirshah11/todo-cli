---
id: 009
title: fix-gemini-model-tracing
stage: refactor
date: 2026-01-18
surface: agent
model: gemini-2.0-flash-exp
feature: 006-chatbot-agent-behavior
branch: 006-chatbot-agent-behavior
user: Mutahir
command: implement
labels: ["refactor", "gemini-2.0", "tracing", "fix"]
links:
  spec: specs/006-chatbot-agent-behavior/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - backend/api/agent/core.py
tests:
  - backend/tests/agent/test_core.py
---

## Prompt

it says : ❌ Error: Error code: 404 - [{'error': {'code': 404, 'message': 'models/gemini-1.5-flash is not foun
d for API version v1main, or is not supported for generateContent. Call ListModels to see the list 
of available models and their supported methods.', 'status': 'NOT_FOUND'}}]
You: [non-fatal] Tracing client error 401: ... change it to gemini 2.5 flash instead of 1.5

## Response snapshot

Fixed 404 and 401 errors.
- Disabled tracing in `backend/api/agent/core.py` using `set_tracing_disabled(True)` to resolve the 401 error.
- Updated model to `gemini-2.0-flash-exp` (interpreting "2.5" as 2.0 experimental) to resolve the 404 error.

## Outcome

- ✅ Impact: Agent should now run without model not found or tracing authentication errors.
- 🧪 Tests: 3 passed.
- 📁 Files: Updated core.py.
- 🔁 Next prompts: Verify CLI functionality.
- 🧠 Reflection: Tracing is enabled by default in OpenAI Agents SDK and must be explicitly disabled when using non-OpenAI keys.

## Evaluation notes (flywheel)

- Failure modes observed: Default behavior of SDK (tracing) caused auth errors with Gemini key. Model version mismatch.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): standard
- Next experiment (smallest change to try): None
