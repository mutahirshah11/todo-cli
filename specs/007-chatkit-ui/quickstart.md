# Quickstart: Chatbot UI

## Development Setup

1. **Install Dependencies**
```bash
cd frontend
npm install @openai/chatkit-react
```

2. **Mock Backend Configuration**
For Phase 3.2, you can mock the `/api/chat/session` endpoint using Next.js Route Handlers:
```typescript
// frontend/src/app/api/chat/session/route.ts
export async function POST() {
  return Response.json({
    client_secret: "mock_secret_...",
    thread_id: "mock_thread_123"
  });
}
```

3. **Verify UI Rendering**
Navigate to `/dashboard/chat` to see the empty state. Send a message to verify input clearing and loading state triggers.

## Testing Scenarios

### Scenario 1: New User
- Clear `localStorage` (if any thread IDs stored).
- Access `/dashboard/chat`.
- Confirm "Welcome" message/tips are visible.

### Scenario 2: History Load
- Mock `/api/chat/session` to return a specific `thread_id`.
- Access the route and confirm ChatKit attempts to fetch history (loading state).
