# API Contracts: Database Integration for Todo Full-Stack Web Application

## Database Integration API Endpoints

### Authentication Service Integration

#### JWT Token Validation
- **Endpoint**: Internal validation using shared secret
- **Method**: Internal function call
- **Input**: JWT token from Authorization header
- **Output**: user_id extracted from token claims
- **Error Responses**: 401 Unauthorized for invalid tokens

### Task Management Endpoints

#### GET /api/v1/tasks
- **Purpose**: Retrieve all tasks for authenticated user
- **Method**: GET
- **Headers**:
  - `Authorization: Bearer <token>`
- **Query Parameters**:
  - `completed`: Optional boolean filter
  - `limit`: Optional integer for pagination
  - `offset`: Optional integer for pagination
- **Response**: 200 OK with array of Task objects
- **Error Responses**:
  - 401 Unauthorized (invalid JWT)
  - 404 Not Found (user does not exist)

#### GET /api/v1/tasks/{id}
- **Purpose**: Retrieve specific task for authenticated user
- **Method**: GET
- **Path Parameters**:
  - `id`: Task ID to retrieve
- **Headers**:
  - `Authorization: Bearer <token>`
- **Response**: 200 OK with single Task object
- **Error Responses**:
  - 401 Unauthorized (invalid JWT)
  - 404 Not Found (task not found)

#### POST /api/v1/tasks
- **Purpose**: Create new task for authenticated user
- **Method**: POST
- **Headers**:
  - `Authorization: Bearer <token>`
  - `Content-Type: application/json`
- **Request Body**:
  ```json
  {
    "title": "Task title (required)",
    "description": "Task description (optional)",
    "completed": false
  }
  ```
- **Response**: 201 Created with created Task object
- **Error Responses**:
  - 400 Bad Request (validation errors)
  - 401 Unauthorized (invalid JWT)

#### PUT /api/v1/tasks/{id}
- **Purpose**: Update existing task for authenticated user
- **Method**: PUT
- **Path Parameters**:
  - `id`: Task ID to update
- **Headers**:
  - `Authorization: Bearer <token>`
  - `Content-Type: application/json`
- **Request Body**:
  ```json
  {
    "title": "Updated task title (optional)",
    "description": "Updated task description (optional)",
    "completed": true
  }
  ```
- **Response**: 200 OK with updated Task object
- **Error Responses**:
  - 400 Bad Request (validation errors)
  - 401 Unauthorized (invalid JWT)
  - 404 Not Found (task not found)

#### PATCH /api/v1/tasks/{id}/complete
- **Purpose**: Toggle completion status of task
- **Method**: PATCH
- **Path Parameters**:
  - `id`: Task ID to update
- **Headers**:
  - `Authorization: Bearer <token>`
  - `Content-Type: application/json`
- **Request Body**:
  ```json
  {
    "completed": true
  }
  ```
- **Response**: 200 OK with updated Task object
- **Error Responses**:
  - 400 Bad Request (validation errors)
  - 401 Unauthorized (invalid JWT)
  - 404 Not Found (task not found)

#### DELETE /api/v1/tasks/{id}
- **Purpose**: Delete task for authenticated user
- **Method**: DELETE
- **Path Parameters**:
  - `id`: Task ID to delete
- **Headers**:
  - `Authorization: Bearer <token>`
- **Response**: 204 No Content
- **Error Responses**:
  - 401 Unauthorized (invalid JWT)
  - 404 Not Found (task not found)

## Database Schema Contracts

### User Table Schema
```sql
CREATE TABLE users (
    user_id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE
);

CREATE INDEX idx_users_email ON users(email);
```

### Task Table Schema
```sql
CREATE TABLE tasks (
    id UUID PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    is_completed BOOLEAN DEFAULT FALSE,
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_completed ON tasks(is_completed);
CREATE INDEX idx_tasks_created_at ON tasks(created_at);
```

## Authentication & Authorization Contracts

### JWT Token Structure
```json
{
  "sub": "user-uuid-string",
  "email": "user@example.com",
  "iat": 1234567890,
  "exp": 1234571490
}
```

### Authorization Validation
- All endpoints require valid JWT token in Authorization header
- User identity is extracted from the JWT token (no user_id in URL path)
- Invalid tokens return 401 Unauthorized
- Non-existent resources return 404 Not Found (no information leak)

## Error Response Format
```json
{
  "detail": "Human-readable error message",
  "error_code": "SYSTEM_DEFINED_ERROR_CODE",
  "timestamp": "ISO 8601 formatted timestamp"
}
```