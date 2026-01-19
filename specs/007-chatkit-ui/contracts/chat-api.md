# Contract: Chat API

## Session Handshake

Initialize a new ChatKit session or resume an existing one.

**Endpoint**: `POST /api/chat/session`

### Request
- **Headers**: `Authorization: Bearer <token>`
- **Body**:
```json
{
  "thread_id": "string (optional)"
}
```

### Response (200 OK)
```json
{
  "client_secret": "string",
  "thread_id": "string"
}
```

## Chat Interaction
Managed internally by ChatKit via the `client_secret`. The frontend does not implement individual POST/GET for messages; instead, it provides the `getClientSecret` callback to the SDK.

### Error Handling
- **401 Unauthorized**: Redirect to login.
- **500 Internal Server Error**: UI renders a global toast via `onError` callback.
