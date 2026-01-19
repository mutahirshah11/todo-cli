# Research: Chatbot User Interface (ChatKit)

## 1. OpenAI ChatKit Library

**Package**: `@openai/chatkit-react`  
**Installation**: `npm install @openai/chatkit-react`

### Core Components
- `<ChatKit />`: The main UI component providing the conversation container, message list, and input.
- `useChatKit()`: A hook to manage chat state, threads, and imperative actions (e.g., `sendUserMessage`, `setThreadId`).

### Authentication Mechanism
ChatKit uses a `client_secret` based handshake:
1. Frontend calls a backend endpoint (`/api/chat/session`).
2. Backend returns a `client_secret`.
3. Frontend provides this secret to the `useChatKit` hook via the `api.getClientSecret` configuration.

## 2. Streaming Support
The library natively supports response streaming when configured with a valid ChatKit session backend. The UI updates progressively as tokens arrive without custom SSE management required in the frontend application layer.

## 3. Interaction Patterns
- **Empty State**: Rendered when `initialThread` is null.
- **Loading State**: Managed via `onResponseStart` and `onResponseEnd` event handlers in `useChatKit`.
- **Error Handling**: Captured via the `onError` callback.

## Decisions
- Use the official `@openai/chatkit-react` bindings.
- Implement a session proxy in the backend (Phase 3.3/3.4 concern, but mocked for 3.2).
- Rely on ChatKit's built-in accessibility and responsive layouts.
