# Implementation Plan: Chatbot User Interface (ChatKit)

**Branch**: `007-chatkit-ui` | **Date**: 2026-01-18 | **Spec**: [specs/007-chatkit-ui/spec.md](../007-chatkit-ui/spec.md)
**Input**: Feature specification from `/specs/007-chatkit-ui/spec.md`

## Summary

Implement a conversational user interface for Phase 3.2 of the Tickwen AI-powered Todo application. This phase focuses on the frontend layer, utilizing OpenAI ChatKit components to enable natural language interaction. The UI will be strictly stateless, deriving all conversation data from backend responses and supporting progressive rendering via Server-Sent Events (SSE).

## Technical Context

**Language/Version**: TypeScript 5.x, React 19 (Next.js 16)  
**Primary Dependencies**: OpenAI ChatKit (React package), Lucide React (Icons), Sonner (Toasts), Tailwind CSS.  
**Storage**: N/A (Stateless UI; derived from backend).  
**Testing**: Jest, React Testing Library.  
**Target Platform**: Modern Browsers (Mobile & Desktop Responsive).
**Project Type**: Web Application (Next.js App Router).  
**Performance Goals**: First contentful paint < 1s, Input responsiveness < 50ms.  
**Constraints**: Zero local state persistence for messages, SSE Streaming support, strictly ChatKit patterns.

## Constitution Check

*GATE: Passed.*

- **Simplicity**: No custom message bubble abstractions; leveraging standard ChatKit components.
- **Privacy**: No local storage of conversation history; session-bound via backend conversation_id.
- **Testability**: Components will be tested for deterministic rendering based on backend message mocks.
- **Extensibility**: Design follows modular React patterns, safe for later 3.3 (Database) and 3.4 (MCP) integration.

## Project Structure

### Documentation (this feature)

```text
specs/007-chatkit-ui/
├── plan.md              # This file
├── research.md          # Phase 0: ChatKit package discovery & SSE setup
├── data-model.md        # Phase 1: Chat Message & Conversation types
├── quickstart.md        # Phase 1: Local development with mock backend
├── contracts/           # Phase 1: Frontend-to-Backend Chat API
│   └── chat-api.md
└── tasks.md             # Phase 2: Implementation tasks (sp.tasks)
```

### Source Code (repository root)

```text
frontend/
├── src/
│   ├── app/
│   │   └── dashboard/
│   │       └── layout.tsx # Hosts FloatingChatbot
│   ├── components/
│   │   ├── chat/        # Feature-specific ChatKit wrappers
│   │   │   ├── chat-container.tsx
│   │   │   └── floating-chatbot.tsx # Toggle logic & positioning
│   │   └── ui/          # Shared toast/primitives
│   └── lib/
│       ├── chat-client.ts # SSE handling logic
│       └── types.ts     # Shared interface definitions
```

**Structure Decision**: Integrated into the `dashboard/layout.tsx` as a floating component to remain accessible across all dashboard views without requiring a dedicated page.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A       |            |                                     |