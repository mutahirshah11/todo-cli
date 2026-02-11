---
name: openai-chatkit
description: |
Engineer high-performance, accessible, and themeable chat interfaces using OpenAI's specialized React ChatKit components.
This skill covers state management via useChat, custom message rendering, streaming optimizations, and integration withagent backends.
Use this when building AI-first UIs that require real-time feedback, message threading, or complex multi-modalinteractions.
---

# OpenAI ChatKit

A professional-grade component library for building immersive AI conversational interfaces.

## Before Implementation

| Source | Gather |
|--------|--------|
| **UI Design** | Theme colors, typography (Tailwind config), and layout (Sidebar vs Full-page). |
| **Backend** | The exact endpoint for SSE streaming (usually `/api/agent/chat`). |
| **Protocols** | Does the backend support Markdown, LaTeX, or custom tool-calling visualization? |

## Quick Start (Advanced Setup)

```tsx
import { ChatKitProvider, MessageList, ChatInput } from '@openai/chatkit-react';
import { useAuth } from '@/hooks/use-auth';

export const AgentChat = () => {
  const { user } = useAuth();

  return (
    <ChatKitProvider 
      endpoint="/api/v1/chat"
      initialMessages={[{ role: 'assistant', content: `Hi ${user?.name}, how can I help?` }]}
    >
      <div className="flex flex-col h-[600px] border rounded-xl overflow-hidden shadow-lg">
        <MessageList className="flex-1 overflow-y-auto p-4 scroll-smooth" />
        <ChatInput 
          className="border-t p-2 bg-muted/50"
          placeholder="Ask me anything..." 
        />
      </div>
    </ChatKitProvider>
  );
};
```

## Core Features

### 1. Unified State Management
The `useChat` hook provides a centralized store for the entire conversation, eliminating the need for custom Redux/Zustand logic for basic chat.

```tsx
const { 
  messages,      // Array of message objects
  loading,       // Boolean for pending responses
  error,         // Error object if stream fails
  sendMessage,   // Function to trigger a new message
  stopStreaming  // Function to abort the current stream
} = useChat();
```

### 2. Intelligent Streaming
ChatKit handles the parsing of `text/event-stream` data automatically, including:
- **Token concatenation:** No flickering during text updates.
- **Auto-scroll:** Stays at the bottom as new content arrives.
- **Handoff tracking:** Detects when a different agent takes over.

### 3. Component Customization
Every component is "headless-capable" or easily styled via `className`.

| Component | Usage |
|-----------|-------|
| `MessageList` | Renders the history. Use `renderMessage` for custom bubbles. |
| `ChatInput` | Handles multi-line input and submit logic. |
| `Suggestion` | Renders clickable chips for quick-start prompts. |

## Advanced Patterns

### Tool Call Visualization
When an agent calls an MCP tool, ChatKit can visualize the "thinking" or "action" state.

```tsx
<MessageList 
  renderMessage={(msg) => (
    <div className="my-2">
      {msg.tool_calls ? <ToolIndicator tools={msg.tool_calls} /> : <p>{msg.content}</p>}
    </div>
  )}
/>
```

### Context Awareness
Passing UI-specific data (like the current page URL or user settings) to the agent via metadata.

```tsx
sendMessage("Analyze this", { 
  metadata: { page: window.location.href, theme: 'dark' } 
});
```

## Best Practices

| Category | Guideline |
|----------|-----------|
| **UX** | Always show a "Stop" button during long generation phases. |
| **Performance** | Use `React.memo` on message components to prevent re-rendering the whole list on every token. |
| **Accessibility** | Ensure the chat input has proper ARIA labels and focus management. |
| **Theming** | Use CSS variables (Tailwind) so the chat matches the app's Light/Dark modes. |

## Anti-Patterns

| Avoid | Why | Instead |
|-------|-----|---------|
| Prop drilling messages | Makes the component tree brittle and hard to maintain. | Use the `useChat` hook in sub-components. |
| Manual string joining | Messy and prone to race conditions during rapid streaming. | Trust the ChatKit internal state. |
| Ignoring 401/403 errors | Users get stuck in a "loading" state forever. | Implement a robust `onError` handler in the Provider. |

## Verification Checklist
- [ ] `ChatKitProvider` has the correct `authHeader` if the API is protected.
- [ ] `MessageList` has `overflow-y-auto` to prevent layout breaks.
- [ ] Markdown content is rendered safely using a library like `react-markdown`.
- [ ] Chat UI is responsive and works on mobile viewports.