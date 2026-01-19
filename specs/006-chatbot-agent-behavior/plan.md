# Implementation Plan - Phase 3.1: AI Agent Behavior

This plan focuses on the **AI Agent Logic** for the Tickwen Todo AI Chatbot. It defines the implementation of a stateless AI agent using the OpenAI Agents SDK (compatible with Gemini API) that interprets user commands and maps them to MCP tools.

## Technical Context

**Language/Framework**: Python, OpenAI Agents SDK (Official).
**LLM**: Gemini (via OpenAI compatibility layer).
**Architecture**: Stateless, Intent-based routing, MCP tool execution.
**Testing**: Pytest (Strict TDD).

### Critical Dependencies
- `openai` (Python SDK)
- `pytest`
- `pydantic` (for tool schemas)

### Unknowns & Risks
- **Gemini Compatibility**: Confirm `AsyncOpenAI` client works seamlessly with Gemini's OpenAI-compatible endpoint for tool calling. [NEEDS CLARIFICATION]
- **Stateless Context Limit**: How much conversation history can be passed before hitting token limits? Need a truncation strategy. [NEEDS CLARIFICATION]
- **Tool Schema Format**: Confirm exact JSON schema structure expected by Gemini models for function calling. [NEEDS CLARIFICATION]

## Constitution Check

| Principle | Compliance Strategy |
| :--- | :--- |
| **Strict TDD** | Tests will be written for intent classification and tool mapping *before* agent logic. |
| **User Privacy** | Agent is stateless; no internal storage. Conversation context is passed per request. |
| **Future Extensibility** | MCP abstraction decouples agent from tool implementation. |
| **Simplicity** | Minimal agent logic: Receive -> Parse -> Call Tool -> Respond. No complex chains. |

## Phases

### Phase 0: Outline & Research

1.  **Research Gemini/OpenAI Compatibility**: Verify tool calling syntax and authentication with Gemini via `AsyncOpenAI`.
2.  **Context Management Strategy**: Define rules for truncating conversation history to fit context windows.
3.  **Tool Schema Definition**: Determine the optimal Pydantic/JSON schema format for the LLM.

### Phase 1: Design & Contracts

1.  **Data Model**: Define `AgentRequest` (User Input + History) and `AgentResponse` (Text + Tool Calls).
2.  **Contracts**: Create JSON schemas for `add_task`, `list_tasks`, `update_task`, `delete_task`, `complete_task`.
3.  **Quickstart**: usage guide for running the agent locally.

### Phase 2: Implementation (TDD)

1.  **Test Suite Setup**: Create `tests/agent/test_agent_behavior.py`.
2.  **Mock Tools**: Implement dummy MCP tools for testing.
3.  **Intent Classification Tests**: Verify agent maps "Buy milk" -> `add_task`.
4.  **Parameter Extraction Tests**: Verify "Call mom tomorrow" -> `due_date`.
5.  **Conversation Context Tests**: Verify "Delete it" uses previous context.
6.  **Agent Implementation**: Build the `Agent` class using `AsyncOpenAI`.

## Gate Checks

- [ ] Research confirms Gemini tool calling works via OpenAI SDK.
- [ ] Tool schemas are defined and validated.
- [ ] Tests cover all User Stories in Spec.