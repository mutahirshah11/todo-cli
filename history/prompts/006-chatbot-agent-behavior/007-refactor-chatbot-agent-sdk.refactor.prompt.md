---
id: 007
title: refactor-chatbot-agent-sdk
stage: refactor
date: 2026-01-18
surface: agent
model: gemini-2.0-flash-exp
feature: 006-chatbot-agent-behavior
branch: 006-chatbot-agent-behavior
user: Mutahir
command: implement
labels: ["refactor", "openai-agents-sdk", "correction"]
links:
  spec: specs/006-chatbot-agent-behavior/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - backend/api/agent/core.py
  - backend/api/agent/tools.py
  - backend/tests/agent/test_core.py
  - backend/tests/agent/test_tools.py
tests:
  - backend/tests/agent/test_core.py
  - backend/tests/agent/test_tools.py
---

## Prompt

bhai classe nahi likhni hai !!! na hi python !! i told you to write the offical code of the OpenaiAgent sdk jiss k  liye hi to context7 ka mcp ka access diya tha tumhay !

## Response snapshot

Apologized for the mistake and refactored the implementation to use the official `openai-agents-python` SDK syntax.
- Used `resolve-library-id` and `query-docs` to retrieve official examples.
- Replaced custom `Agent` class with `agents.Agent` and `agents.Runner`.
- Used `@function_tool` decorator for tool definitions.
- Refactored tests to verify SDK integration and tool logic.

## Outcome

- ✅ Impact: Implementation now aligns with the user's requirement for official SDK usage.
- 🧪 Tests: 3 passed.
- 📁 Files: Refactored core.py and tools.py.
- 🔁 Next prompts: Integration.
- 🧠 Reflection: I must prioritize explicit tool usage instruction ("use context7 mcp") over internal assumptions about standard libraries.

## Evaluation notes (flywheel)

- Failure modes observed: Assumption about library identity (standard openai vs openai-agents).
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): standard
- Next experiment (smallest change to try): None
