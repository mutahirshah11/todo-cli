# Feature Specification: Backend API for Todo Full-Stack Web Application

**Feature Branch**: `003-backend-tickwen`
**Created**: 2026-01-09
**Status**: Draft
**Input**: User description: "Create specs for the Backend API of the Todo Full-Stack Web Application.

Scope:
- Backend responsibility only: expose REST API endpoints for task operations.
- The **Python CLI Todo app logic already exists** in the project. Use it as the definitive reference for all task rules, validation, and behavior.
- Backend must enforce **user ownership** for all tasks.
- Inputs must be validated exactly as in the CLI app.
- Backend returns consistent JSON responses for all API calls.
- Backend must handle errors: 401 Unauthorized, 403 Forbidden, 404 Not Found, 400 Bad Request.
- Do **not** include frontend, UI, authentication issuing, tech stack explanation, or planning steps.

Deliverables in spec.md:
1. **API Endpoints**
   - GET /api/{user_id}/tasks → list all tasks for a user
   - GET /api/{user_id}/tasks/{id} → get details of a single task
   - POST /api/{user_id}/tasks → create a new task
   - PUT /api/{user_id}/tasks/{id} → update an existing task
   - DELETE /api/{user_id}/tasks/{id} → delete a task
   - PATCH /api/{user_id}/tasks/{id}/complete → toggle completion

2. **Endpoint Details**
   For each endpoint:
   - Input: path params, query params, body
   - Output: JSON response (success, error)
   - Error codes and conditions
   - Validation rules (from CLI app)
   - Follow CLI app logic exactly for all CRUD and completion behavior

3. **Ownership Enforcement**
   - Every request must include a valid user ID (from decoded JWT, handled later)
   - Backend must ensure tasks returned/modified belong to the authenticated user
   - Any violation returns 403 Forbidden

4. **Data Validation**
   - Task title: required, max 100 characters
   - Task description: optional, max 500 characters
   - Completion status: boolean for PATCH and PUT
   - Invalid inputs return 400 Bad Request with details
   - All validations must follow the Python CLI Todo logic exactly

5. **Error Handling**
   - 401 Unauthorized if user ID is missing/invalid (token verification later)
   - 403 Forbidden if task does not belong to user
   - 404 Not Found if task ID does not exist
   - 400 Bad Request for invalid payloads
   - All error responses must include JSON with { "error": "<message>" }

6. **Output Requirements**
   - spec.md must have structured sections:
     1. API Endpoints
     2. Endpoint Details
     3. Ownership Enforcement
     4. Data Validation
     5. Error Handling
   - Include **sample JSON request and response** for each endpoint
   - Python CLI logic is the source of truth for task behavior, validations, and rules
   - Do not include frontend logic, JWT issuance, or deployment details"

## API Endpoints

The backend API will expose the following REST endpoints for task operations:

- **GET** `/api/{user_id}/tasks` → List all tasks for a user
- **GET** `/api/{user_id}/tasks/{id}` → Get details of a single task
- **POST** `/api/{user_id}/tasks` → Create a new task
- **PUT** `/api/{user_id}/tasks/{id}` → Update an existing task
- **DELETE** `/api/{user_id}/tasks/{id}` → Delete a task
- **PATCH** `/api/{user_id}/tasks/{id}/complete` → Toggle completion status

## Endpoint Details

### 1. GET /api/{user_id}/tasks → List all tasks for a user

**Input:**
- Path Parameters: `user_id` (string) - The ID of the authenticated user
- Query Parameters: None

**Output:**
- Success Response (200 OK): Array of task objects in JSON format
- Error Responses: 401, 403, 404 (as defined in Error Handling)

**Sample Request:**
```
GET /api/12345/tasks
Authorization: Bearer <jwt_token>
```

**Sample Response:**
```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Complete project",
      "description": "Finish the backend API specification",
      "completed": false,
      "created_at": "2026-01-09T10:00:00Z",
      "updated_at": "2026-01-09T10:00:00Z",
      "user_id": "12345"
    },
    {
      "id": 2,
      "title": "Review code",
      "description": "Check the implementation against spec",
      "completed": true,
      "created_at": "2026-01-09T09:30:00Z",
      "updated_at": "2026-01-09T10:15:00Z",
      "user_id": "12345"
    }
  ]
}
```

---

### 2. GET /api/{user_id}/tasks/{id} → Get details of a single task

**Input:**
- Path Parameters: `user_id` (string), `id` (string) - The task ID
- Query Parameters: None

**Output:**
- Success Response (200 OK): Single task object in JSON format
- Error Responses: 401, 403, 404 (as defined in Error Handling)

**Sample Request:**
```
GET /api/12345/tasks/1
Authorization: Bearer <jwt_token>
```

**Sample Response:**
```json
{
  "task": {
    "id": 1,
    "title": "Complete project",
    "description": "Finish the backend API specification",
    "completed": false,
    "created_at": "2026-01-09T10:00:00Z",
    "updated_at": "2026-01-09T10:00:00Z",
    "user_id": "12345"
  }
}
```

---

### 3. POST /api/{user_id}/tasks → Create a new task

**Input:**
- Path Parameters: `user_id` (string) - The ID of the authenticated user
- Request Body (JSON): Task object containing title, description, and completed status
- Headers: Authorization header with JWT token

**Output:**
- Success Response (201 Created): Created task object in JSON format
- Error Responses: 400, 401, 403 (as defined in Error Handling)

**Sample Request:**
```json
POST /api/12345/tasks
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "title": "New task",
  "description": "Task description",
  "completed": false
}
```

**Sample Response:**
```json
{
  "task": {
    "id": 3,
    "title": "New task",
    "description": "Task description",
    "completed": false,
    "created_at": "2026-01-09T11:00:00Z",
    "updated_at": "2026-01-09T11:00:00Z",
    "user_id": "12345"
  }
}
```

---

### 4. PUT /api/{user_id}/tasks/{id} → Update an existing task

**Input:**
- Path Parameters: `user_id` (string), `id` (string) - The task ID
- Request Body (JSON): Task object containing updated fields
- Headers: Authorization header with JWT token

**Output:**
- Success Response (200 OK): Updated task object in JSON format
- Error Responses: 400, 401, 403, 404 (as defined in Error Handling)

**Sample Request:**
```json
PUT /api/12345/tasks/1
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "title": "Updated task title",
  "description": "Updated task description",
  "completed": true
}
```

**Sample Response:**
```json
{
  "task": {
    "id": 1,
    "title": "Updated task title",
    "description": "Updated task description",
    "completed": true,
    "created_at": "2026-01-09T10:00:00Z",
    "updated_at": "2026-01-09T11:30:00Z",
    "user_id": "12345"
  }
}
```

---

### 5. DELETE /api/{user_id}/tasks/{id} → Delete a task

**Input:**
- Path Parameters: `user_id` (string), `id` (string) - The task ID
- Headers: Authorization header with JWT token

**Output:**
- Success Response (204 No Content): Empty response body
- Error Responses: 401, 403, 404 (as defined in Error Handling)

**Sample Request:**
```
DELETE /api/12345/tasks/1
Authorization: Bearer <jwt_token>
```

**Sample Response:**
```
Status: 204 No Content
```

---

### 6. PATCH /api/{user_id}/tasks/{id}/complete → Toggle completion status

**Input:**
- Path Parameters: `user_id` (string), `id` (string) - The task ID
- Request Body (JSON): Object containing completion status
- Headers: Authorization header with JWT token

**Output:**
- Success Response (200 OK): Updated task object in JSON format
- Error Responses: 400, 401, 403, 404 (as defined in Error Handling)

**Sample Request:**
```json
PATCH /api/12345/tasks/1/complete
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "completed": true
}
```

**Sample Response:**
```json
{
  "task": {
    "id": 1,
    "title": "Complete project",
    "description": "Finish the backend API specification",
    "completed": true,
    "created_at": "2026-01-09T10:00:00Z",
    "updated_at": "2026-01-09T12:00:00Z",
    "user_id": "12345"
  }
}
```

## Ownership Enforcement

- Every API request must include a valid user ID, which will be extracted from the decoded JWT token
- The backend must verify that any task being accessed (read, updated, deleted) belongs to the authenticated user
- If a user attempts to access a task that does not belong to them, the API must return a 403 Forbidden error
- The user ID in the path parameter must match the user ID in the JWT token for all operations
- All validation rules must follow the Python CLI Todo app logic exactly

## Data Validation

- **Task Title**: Required field, maximum 100 characters
- **Task Description**: Optional field, maximum 500 characters
- **Completion Status**: Boolean value for PATCH and PUT operations
- **Invalid inputs** must return a 400 Bad Request error with specific validation details
- All validations must follow the Python CLI Todo app logic exactly
- All validation errors must return JSON in the format: `{ "error": "<validation_message>" }`

## Error Handling

- **401 Unauthorized**: Returned when user ID is missing or invalid (JWT token verification fails)
- **403 Forbidden**: Returned when a task does not belong to the authenticated user
- **404 Not Found**: Returned when the requested task ID does not exist
- **400 Bad Request**: Returned when request payload contains invalid data
- All error responses must include JSON with the format: `{ "error": "<descriptive_error_message>" }`

**Sample Error Responses:**
```json
{
  "error": "Unauthorized access - invalid or missing token"
}
```

```json
{
  "error": "Forbidden - task does not belong to user"
}
```

```json
{
  "error": "Task not found with id: 123"
}
```

```json
{
  "error": "Title is required and cannot exceed 100 characters"
}
```

## Clarifications

### Session 2026-01-09

- Q: What are the expected response time targets for the API endpoints? → A: Target 95th percentile response time of <100ms for all endpoints
- Q: How should the API handle concurrent modifications to the same task by the same user? → A: Optimistic locking: reject updates if the task was modified since last read (using version/etag)
- Q: What is the expected data retention policy for user tasks in the system? → A: Indefinite retention - user tasks stored permanently unless explicitly deleted by user
- Q: What rate limiting policy should be applied to the API endpoints? → A: Per-user rate limiting: 1000 requests per hour per user per endpoint
- Q: What audit logging is required for user task operations? → A: Full audit trail: log all task operations (create, read, update, delete) with user ID, timestamp, IP address

## Non-Functional Requirements

- **Performance**: Target 95th percentile response time of <100ms for all endpoints
- **Concurrency**: Optimistic locking - reject updates if the task was modified since last read (using version/etag)
- **Data Retention**: Indefinite retention - user tasks stored permanently unless explicitly deleted by user
- **Rate Limiting**: Per-user rate limiting: 1000 requests per hour per user per endpoint
- **Audit Logging**: Full audit trail: log all task operations (create, read, update, delete) with user ID, timestamp, IP address