---
name: fastapi-framework
description: This skill provides comprehensive guidance on FastAPI framework for building async REST APIs with automatic documentation and type safety. It should be used when users need guidance on FastAPI app setup, routing, dependency injection, middleware, error handling, async patterns, Pydantic models, CORS configuration, authentication, background tasks, WebSockets, file uploads, and API documentation.
---

# FastAPI Framework Guide

This skill provides comprehensive guidance on FastAPI framework for building async REST APIs with automatic documentation and type safety. It covers FastAPI app setup, routing, dependency injection, middleware, error handling, async patterns, Pydantic models, CORS configuration, authentication, background tasks, WebSockets, file uploads, and API documentation.

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Existing FastAPI project structure, dependencies, and patterns to integrate with |
| **Conversation** | User's specific API requirements, authentication needs, database setup, and deployment environment |
| **Skill References** | FastAPI patterns from `references/` (routing, dependencies, middleware, async patterns) |
| **User Guidelines** | Project-specific conventions, security requirements, team standards |

Ensure all required context is gathered before implementing.

## FastAPI Fundamentals

### App Setup and Structure
- Create FastAPI instance: `app = FastAPI()`
- Typical project structure:
```
project/
├── main.py              # Main application entry point
├── models/              # Pydantic models
├── schemas/             # Request/response schemas
├── routers/             # API route modules
├── database/            # Database connection logic
├── middleware/          # Custom middleware
└── utils/               # Utility functions
```
- Use `uvicorn main:app --reload` to run development server

### Core Benefits
- Automatic interactive API documentation (Swagger UI and ReDoc)
- Built-in data validation with Pydantic
- Type hints support for better IDE experience
- High performance with Starlette and async/await
- Dependency injection system

## Routing and Parameters

### Route Definition
- Use decorators corresponding to HTTP methods:
  - `@app.get("/")` for GET requests
  - `@app.post("/items/")` for POST requests
  - `@app.put("/items/{id}")` for PUT requests
  - `@app.delete("/items/{id}")` for DELETE requests

### Path Parameters
- Extract from URL path: `/users/{user_id}`
- Automatically validated with type hints:
```python
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    return {"user_id": user_id}
```

### Query Parameters
- Extract from URL query string
- Use optional types or default values:
```python
@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 100, q: str = None):
    return {"skip": skip, "limit": limit, "q": q}
```

### Request Body with Pydantic Models
- Define request schemas using Pydantic models:
```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

@app.post("/items/")
async def create_item(item: Item):
    return item
```

### Response Models
- Declare response models for validation and documentation:
```python
@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    return item  # Will be validated against Item model
```

## Dependency Injection

### Basic Dependencies
- Use `Depends()` to inject dependencies:
```python
def get_current_user(token: str = Depends(oauth2_scheme)):
    return User(username="john_doe")

@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
```

### Shared Dependencies
- Create reusable dependencies for authentication, database sessions, etc.
- Dependencies can have sub-dependencies
- Use class-based dependencies for more complex scenarios

### Security Dependencies
- OAuth2 with password flow
- API key authentication
- JWT token validation
- Session-based authentication

## Middleware Configuration

### CORS Middleware
- Configure allowed origins for frontend integration:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
```

### Custom Middleware
- Process requests and responses
- Add custom headers, logging, authentication
```python
@app.middleware("http")
async def add_process_time_header(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

### Third-party Middleware
- Rate limiting
- Request/response compression
- Security headers
- Request logging

## Error Handling

### HTTPException
- Raise HTTP errors with specific status codes:
```python
from fastapi import HTTPException

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id": item_id}
```

### Custom Exception Handlers
- Handle specific exceptions globally:
```python
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()}
    )
```

### Business Logic Errors
- Create custom exception classes
- Use proper HTTP status codes
- Provide meaningful error messages

## Async Patterns and Performance

### Async/Await Best Practices
- Use `async def` for I/O-bound operations
- Use `def` for CPU-bound operations (avoids blocking event loop)
- Leverage connection pooling for databases
- Use async database drivers when available

### Background Tasks
- Execute tasks after returning response:
```python
from fastapi import BackgroundTasks

def send_email_task(email: str, message: str):
    # Simulate sending email
    time.sleep(5)
    print(f"Email sent to {email}")

@app.post("/send-email/")
async def send_email(background_tasks: BackgroundTasks, email: str, message: str):
    background_tasks.add_task(send_email_task, email, message)
    return {"message": "Email will be sent in the background"}
```

### Performance Optimization
- Use connection pooling
- Implement caching mechanisms
- Optimize database queries
- Use proper indexing

## API Documentation

### Automatic Documentation
- Swagger UI available at `/docs`
- ReDoc available at `/redoc`
- OpenAPI schema at `/openapi.json`
- All endpoints automatically documented based on type hints

### Custom Documentation
- Add metadata to endpoints:
```python
@app.get(
    "/items/",
    tags=["items"],
    summary="List items",
    description="Get a list of items with optional filtering",
    response_description="List of items"
)
async def read_items():
    return items
```

### API Versioning
- Use URL prefixes: `/v1/items/`, `/v2/items/`
- Implement APIRouter for version management
- Maintain backward compatibility

## Common Scenarios

### CRUD Operations
- Create: POST request with request body
- Read: GET request with path/query parameters
- Update: PUT/PATCH request with partial/full updates
- Delete: DELETE request with path parameter

### Authentication Endpoint
- OAuth2 with password flow
- JWT token generation and validation
- Refresh token implementation
- Session management

### File Upload Endpoint
- Handle binary file uploads
- Validate file types and sizes
- Save files securely
- Return upload status

### Webhook Receiver
- Validate webhook signatures
- Process payload asynchronously
- Return appropriate status codes
- Handle retries and errors

### Background Job Trigger
- Accept job parameters
- Queue background tasks
- Return job status/ID
- Monitor job progress

## Best Practices

### Use async def for all routes (performance)
- Leverages asyncio for concurrency
- Improves I/O performance
- Better resource utilization

### Define response models (type safety, docs)
- Ensures consistent response structure
- Automatic validation
- Better API documentation

### Use dependency injection (don't repeat yourself)
- Promotes code reuse
- Simplifies testing
- Improves maintainability

### Handle errors with HTTPException
- Proper HTTP status codes
- Consistent error format
- Meaningful error messages

### Enable CORS properly
- Restrict allowed origins
- Configure credentials appropriately
- Limit allowed methods and headers

### Version your API (/v1/)
- Use URL prefixes for versioning
- Maintain backward compatibility
- Document breaking changes

## Pydantic v2 Features

### Enhanced Validation
- Improved error messages
- Better performance
- More validation options

### Type Annotations
- Use `Annotated` for metadata:
```python
from typing_extensions import Annotated
from pydantic import Field

@app.get("/items/{item_id}")
async def read_item(
    item_id: Annotated[int, Path(title="The ID of the item to get")]
):
    return {"item_id": item_id}
```

### Model Configuration
- Custom validation rules
- Serialization options
- Field constraints and defaults

## APIRouter for Modular Routes

### Organizing Routes
- Separate routes by functionality
- Use consistent prefixes
- Group related endpoints
```python
from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/")
async def get_users():
    return [{"username": "johndoe"}]

app.include_router(router)
```

### Modular Project Structure
- Split large applications into multiple routers
- Maintain clear separation of concerns
- Improve code organization and maintainability