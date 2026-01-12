# API Contract: Authentication Endpoints

## Auth Registration Endpoint
```
POST /api/auth/register
```

### Request
**Headers**:
- `Content-Type: application/json`

**Body**:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "confirm_password": "SecurePass123!"
}
```

**Validation**:
- Email: Valid email format
- Password: Minimum 8 characters with mixed case, numbers, and special characters
- Confirm Password: Must match password

### Response
**Success (201 Created)**:
```json
{
  "success": true,
  "user": {
    "id": "uuid-string",
    "email": "user@example.com",
    "created_at": "2026-01-11T10:00:00Z"
  },
  "token": {
    "access_token": "jwt-token-string",
    "token_type": "bearer",
    "expires_in": 3600
  }
}
```

**Error (400 Bad Request)**:
```json
{
  "error": "Validation Error",
  "message": "Invalid email format or password requirements not met",
  "code": "AUTH_003"
}
```

**Error (409 Conflict)**:
```json
{
  "error": "Conflict",
  "message": "User with this email already exists",
  "code": "AUTH_004"
}
```

---

## Auth Login Endpoint
```
POST /api/auth/login
```

### Request
**Headers**:
- `Content-Type: application/json`

**Body**:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

### Response
**Success (200 OK)**:
```json
{
  "success": true,
  "user": {
    "id": "uuid-string",
    "email": "user@example.com"
  },
  "token": {
    "access_token": "jwt-token-string",
    "token_type": "bearer",
    "expires_in": 3600
  }
}
```

**Error (401 Unauthorized)**:
```json
{
  "error": "Unauthorized",
  "message": "Invalid credentials",
  "code": "AUTH_001"
}
```

---

## Get Current User Endpoint
```
GET /api/auth/me
```

### Request
**Headers**:
- `Authorization: Bearer {jwt_token}`

### Response
**Success (200 OK)**:
```json
{
  "user": {
    "id": "uuid-string",
    "email": "user@example.com",
    "created_at": "2026-01-11T10:00:00Z"
  }
}
```

**Error (401 Unauthorized)**:
```json
{
  "error": "Unauthorized",
  "message": "Invalid or missing authentication token",
  "code": "AUTH_001"
}
```

---

## Protected Task Endpoints

### Get User's Tasks
```
GET /api/v1/{user_id}/tasks
```

### Request
**Headers**:
- `Authorization: Bearer {jwt_token}`

**Path Parameters**:
- `user_id`: The ID of the user whose tasks to retrieve (must match JWT user_id)

### Response
**Success (200 OK)**:
```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Sample Task",
      "description": "Task description",
      "completed": false,
      "created_at": "2026-01-11T10:00:00Z",
      "user_id": "uuid-string"
    }
  ]
}
```

**Error (401 Unauthorized)**:
```json
{
  "error": "Unauthorized",
  "message": "Invalid or missing authentication token",
  "code": "AUTH_001"
}
```

**Error (403 Forbidden)**:
```json
{
  "error": "Forbidden",
  "message": "Access denied - insufficient permissions",
  "code": "AUTH_002"
}
```

### Additional Protected Endpoints
All other task endpoints (`POST /api/v1/{user_id}/tasks`, `PUT /api/v1/{user_id}/tasks/{id}`, `DELETE /api/v1/{user_id}/tasks/{id}`, `PATCH /api/v1/{user_id}/tasks/{id}/complete`) follow the same authentication pattern with identical error responses.