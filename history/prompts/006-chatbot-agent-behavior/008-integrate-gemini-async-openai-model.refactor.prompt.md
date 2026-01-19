---
id: 008
title: integrate-gemini-async-openai-model
stage: refactor
date: 2026-01-18
surface: agent
model: gemini-2.0-flash-exp
feature: 006-chatbot-agent-behavior
branch: 006-chatbot-agent-behavior
user: Mutahir
command: implement
labels: ["refactor", "gemini", "async-openai", "openai-chat-completion-model"]
links:
  spec: specs/006-chatbot-agent-behavior/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - backend/api/agent/core.py
  - run_agent_cli.py
tests:
  - backend/tests/agent/test_core.py
  - backend/tests/agent/test_tools.py
---

## Prompt

bhai as i told you we have to use Gemini Api key with Openaichatcompletionmodel and AyncOpenai to us k hisaab sae karo

## Response snapshot

Refactored `backend/api/agent/core.py` to use `AsyncOpenAI` client with Gemini's base URL and the `OpenAIChatCompletionsModel` from the OpenAI Agents SDK.
- Configured `AsyncOpenAI` with `GEMINI_API_KEY`.
- Instantiated `OpenAIChatCompletionsModel` using the custom client.
- Handled missing API keys during module import to prevent test collection failures.
- Updated the CLI test script to reference `GEMINI_API_KEY`.

## Outcome

- ✅ Impact: Backend agent now uses the exact requested model/client configuration for Gemini compatibility.
- 🧪 Tests: 3 passed.
- 📁 Files: Updated core.py and run_agent_cli.py.
- 🔁 Next prompts: Integration with database.
- 🧠 Reflection: Explicitly using the model class and custom client is the correct way to handle multi-provider support in the OpenAI Agents SDK.

## Evaluation notes (flywheel)

- Failure modes observed: TypeError due to incorrect parameter name (client vs openai_client).
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): standard
- Next experiment (smallest change to try): None
