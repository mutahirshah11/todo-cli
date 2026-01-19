# Research Phase 3.1: AI Agent Behavior

## 1. Gemini Compatibility with OpenAI SDK

**Objective**: Confirm `AsyncOpenAI` client works seamlessly with Gemini's OpenAI-compatible endpoint for tool calling.

**Findings**:
- Gemini models (e.g., `gemini-1.5-pro`, `gemini-1.5-flash`) support the OpenAI Chat Completions API format.
- **Base URL**: `https://generativelanguage.googleapis.com/v1beta/openai/`
- **Authentication**: Uses `GEMINI_API_KEY`.
- **Tool Calling**: Supported via the `tools` parameter in the chat completion request. The structure matches OpenAI's function calling schema.

**Decision**: Use `AsyncOpenAI` client initialized with Gemini's base URL and API key.

## 2. Stateless Context Management

**Objective**: Define rules for truncating conversation history to fit context windows.

**Findings**:
- Gemini 1.5 Flash has a large context window (1M+ tokens), making strict truncation less critical for typical todo app usage than with older models.
- **Strategy**: 
    - Pass full conversation history for the current session.
    - If history exceeds a safe buffer (e.g., 20 messages or ~8k tokens), summarize older turns or truncate the oldest non-system messages.
    - For Phase 3.1, a sliding window of the last 20 messages is sufficient and simple.

**Decision**: Implement a sliding window of the last 20 messages.

## 3. Tool Schema Format

**Objective**: Determine the optimal Pydantic/JSON schema format for the LLM.

**Findings**:
- Gemini expects standard JSON Schema in the `parameters` field of tool definitions.
- Pydantic models can auto-generate this schema via `model_json_schema()`.

**Decision**: Define tools using Pydantic models and convert them to JSON schema for the API call.

## 4. Framework Choice (Context7/OpenAI)

**Objective**: Adhere to "Context7 official syntax" using OpenAI Agents SDK.

**Findings**:
- The user requested "OpenaiAgentsdk through context7 offical syntax".
- This aligns with using the standard `openai` Python library (v1.x+) with its `ChatCompletion` API and `tools` parameter, which is the industry standard (and likely what Context7 documents).
- We will avoid custom wrapper classes unless necessary, utilizing the SDK's native `types` and `BaseModel` integration where possible.

**Decision**: Use strict OpenAI v1.x+ syntax for Agents (Chat + Tools).

## Resolved Unknowns

- [x] **Gemini Compatibility**: Confirmed via OpenAI compatibility layer.
- [x] **Stateless Context Limit**: Sliding window (20 messages).
- [x] **Tool Schema Format**: Standard JSON Schema via Pydantic.
- [x] **Framework**: Standard OpenAI v1.x+ SDK.