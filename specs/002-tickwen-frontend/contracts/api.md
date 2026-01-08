# API Contract: Tickwen Backend

**Feature**: 002-tickwen-frontend

This document defines the expected API endpoints and behavior for the backend integration.
**Base URL**: `/api/`
**Auth**: `Authorization: Bearer <token>` required for all endpoints.

## Endpoints

### 1. Fetch Tasks
- **GET** `/api/{user_id}/tasks`
- **Description**: Fetch all tasks for the specific user.
- **Headers**: `Authorization: Bearer <token>`
- **Response 200 (OK)**:
  ```json
  [
    {
      "id": "uuid",
      "title": "Buy milk",
      "description": "2% fat",
      "is_completed": false,
      "created_at": "2026-01-01T10:00:00Z"
    }
  ]
  ```
- **Response 401**: Unauthorized.

### 2. Fetch Single Task
- **GET** `/api/{user_id}/tasks/{id}`
- **Response 200 (OK)**: Single Task object.
- **Response 404**: Not Found.

### 3. Create Task
- **POST** `/api/{user_id}/tasks`
- **Body**:
  ```json
  {
    "title": "New Task",
    "description": "Optional"
  }
  ```
- **Response 201 (Created)**: Created Task object.

### 4. Update Task
- **PUT** `/api/{user_id}/tasks/{id}`
- **Body**: (Partial or Full update)
  ```json
  {
    "title": "Updated Title",
    "description": "Updated Description",
    "is_completed": true
  }
  ```
- **Response 200 (OK)**: Updated Task object.

### 5. Toggle Completion
- **PATCH** `/api/{user_id}/tasks/{id}/complete`
- **Body**: Empty or specific status payload (Spec implies just toggle endpoint, but safer to assume it might take status or just toggle).
- **Assumption**: Backend toggles the status.
- **Response 200 (OK)**: Updated Task object.

### 6. Delete Task
- **DELETE** `/api/{user_id}/tasks/{id}`
- **Response 204**: No Content (Success).

## Error Formats
Standard Error Response:
```json
{
  "error": "Error message",
  "code": "ERROR_CODE"
}
```
