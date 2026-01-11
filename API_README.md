# Todo API Backend

This is a FastAPI-based REST API for the Todo Full-Stack Web Application. It exposes endpoints that wrap the existing Python CLI todo functionality.

## Features

- RESTful API endpoints for task management
- JWT-based authentication and authorization
- User ownership enforcement
- Input validation matching CLI app logic
- Consistent JSON responses
- Error handling with appropriate status codes

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/{user_id}/tasks` | List all tasks for a user |
| GET | `/api/{user_id}/tasks/{id}` | Get details of a single task |
| POST | `/api/{user_id}/tasks` | Create a new task |
| PUT | `/api/{user_id}/tasks/{id}` | Update an existing task |
| DELETE | `/api/{user_id}/tasks/{id}` | Delete a task |
| PATCH | `/api/{user_id}/tasks/{id}/complete` | Toggle completion status |

## Installation

1. Install the dependencies:
   ```bash
   pip install -e .
   ```

2. Set up environment variables:
   ```bash
   # Copy the example environment file
   cp .env.example .env

   # Edit the .env file with your configuration
   ```

## Running the API

Start the development server:

```bash
uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.

## Authentication

All endpoints require a valid JWT token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

The token must contain a `user_id` claim that matches the `user_id` in the URL path.

## Error Handling

The API returns appropriate HTTP status codes:

- `200`: Success for GET, PUT, PATCH requests
- `201`: Created for successful POST requests
- `204`: No Content for successful DELETE requests
- `400`: Bad Request for validation errors
- `401`: Unauthorized for missing or invalid tokens
- `403`: Forbidden for user ownership violations
- `404`: Not Found for missing resources

Error responses follow the format: `{"error": "error message"}`

## Example Usage

### Create a Task

```bash
curl -X POST http://localhost:8000/api/user123/tasks \
  -H "Authorization: Bearer <your-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Buy groceries",
    "description": "Milk, bread, eggs",
    "completed": false
  }'
```

### Get All Tasks

```bash
curl -X GET http://localhost:8000/api/user123/tasks \
  -H "Authorization: Bearer <your-token>"
```

## Data Validation

- **Title**: Required, maximum 100 characters
- **Description**: Optional, maximum 500 characters
- **Completed**: Boolean value