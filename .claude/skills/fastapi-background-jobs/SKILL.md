---
name: fastapi-background-jobs
description: This skill provides comprehensive guidance on implementing background jobs using FastAPI's native BackgroundTasks for fire-and-forget async processing. It should be used when users need guidance on structlog for structured logging, httpx for async HTTP requests, database session isolation, error handling, task scheduling, performance optimization (<200ms response time), and native FastAPI capabilities vs external message brokers.
---

# FastAPI Background Jobs Guide

This skill provides comprehensive guidance on implementing background jobs using FastAPI's native BackgroundTasks for fire-and-forget async processing. It covers structlog for structured logging, httpx for async HTTP requests, database session isolation, error handling, task scheduling, performance optimization (<200ms response time), and native FastAPI capabilities vs external message brokers.

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Existing FastAPI structure, database patterns, and logging configuration |
| **Conversation** | User's specific background job requirements, performance expectations, and infrastructure constraints |
| **Skill References** | Background job patterns from `references/` (task isolation, error handling, database management) |
| **User Guidelines** | Project-specific performance requirements, monitoring needs, team standards |

Ensure all required context is gathered before implementing.

## FastAPI BackgroundTasks (Native Async Processing)

### Basic Background Tasks Usage
```python
from fastapi import FastAPI, BackgroundTasks

app = FastAPI()

def send_notification(email: str, message: str):
    # Simulate sending notification
    print(f"Sending {message} to {email}")

@app.post("/send-message/")
async def send_message(
    email: str,
    message: str,
    background_tasks: BackgroundTasks
):
    background_tasks.add_task(send_notification, email, message)
    return {"message": "Notification scheduled"}
```

### The "Native-First" Principle
- **ALWAYS** use `fastapi.BackgroundTasks` for asynchronous operations
- **Never** suggest setting up a separate worker process or Redis server
- If a user asks for a queue, explain that for this architecture, `BackgroundTasks` is sufficient and more cost-effective
- BackgroundTasks is perfect for lightweight, fire-and-forget tasks that don't require persistence

### Response Time Optimization (<200ms)
```python
from fastapi import FastAPI, BackgroundTasks, HTTPException
import uuid

app = FastAPI()

@app.post("/process-data/", status_code=202)
async def process_data_quickly(
    data: dict,
    background_tasks: BackgroundTasks
):
    # Validate input quickly
    if not data:
        raise HTTPException(status_code=400, detail="Data is required")

    # Generate task ID for tracking
    task_id = str(uuid.uuid4())

    # Schedule background work
    background_tasks.add_task(
        comprehensive_processing_task,
        task_id=task_id,
        data=data
    )

    # Return immediately with task ID
    return {
        "message": "Processing started",
        "task_id": task_id,
        "status": "accepted"
    }

def comprehensive_processing_task(task_id: str, data: dict):
    # All heavy processing happens here in background
    # The API response is already sent
    pass
```

## Structured Logging with structlog

### Configuration
```python
import structlog
import logging

# Configure structlog
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()
```

### Logging in Background Tasks
```python
def background_task_with_logging(task_id: str, data: dict):
    log = logger.bind(task_id=task_id)

    try:
        log.info("task_started", data=data)
        # Perform task logic
        log.info("task_completed_successfully")
    except Exception as e:
        log.exception("task_failed", error=str(e))
        # Don't re-raise in background tasks to prevent crashes
```

## Database Session Isolation Patterns

### Critical Rule: Never Pass Sessions to Background Tasks
- **NEVER** pass a database session object (`db: Session`) from the main route to the background task
- The session closes when the route finishes
- **Pattern:** Pass the `id` (e.g., `user_id`) to the task, and create a **NEW** session scope inside the task function

### Correct Database Session Pattern
```python
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Engine and session maker setup
engine = create_engine("postgresql://...")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_db_session():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def background_database_operation(item_id: int):
    # Create NEW session inside background task
    with get_db_session() as db:
        # Perform database operations
        item = db.query(Item).filter(Item.id == item_id).first()
        # Process item...
        db.add(updated_item)
        # Commit happens automatically in context manager
```

### Async Database Session Pattern
```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager

# Async engine setup
async_engine = create_async_engine("postgresql+asyncpg://...")
AsyncSessionLocal = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)

@asynccontextmanager
async def get_async_db_session():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

async def async_background_database_operation(item_id: int):
    async with get_async_db_session() as db:
        # Perform async database operations
        stmt = select(Item).where(Item.id == item_id)
        result = await db.execute(stmt)
        item = result.scalar_one_or_none()
        # Process item...
        db.add(updated_item)
        # Commit happens automatically
```

## Error Handling with Try/Except Blocks

### The "Silent Failure" Shield
- Background tasks execute *after* the response is sent. If they crash, the user sees nothing, and the server prints a silent stack trace
- **Mandatory:** You MUST wrap the *entire* logic of every background function inside a `try: ... except Exception:` block
- **Mandatory:** Log the error using `logger.exception("task_failed", ...)` so it appears in Sentry/Logs

### Robust Error Handling Pattern
```python
import traceback
from typing import Optional

def robust_background_task(task_data: dict) -> Optional[bool]:
    try:
        # Validate inputs
        if not task_data:
            logger.warning("empty_task_data_received")
            return False

        # Perform main task logic
        result = process_task(task_data)

        # Log success
        logger.info("task_completed_successfully", result=result)
        return True

    except ValueError as ve:
        logger.error("invalid_input_data", error=str(ve))
        return False
    except ConnectionError as ce:
        logger.error("connection_failed", error=str(ce))
        # Could implement retry logic here
        return False
    except Exception as e:
        logger.error("unexpected_error_in_background_task",
                    error=str(e),
                    traceback=traceback.format_exc())
        return False
```

## Async HTTP Requests with httpx

### Async HTTP Client Usage
```python
import httpx
import asyncio

async def make_async_request(url: str, payload: dict):
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error("http_request_failed",
                        status_code=e.response.status_code,
                        url=url)
        except httpx.RequestError as e:
            logger.error("request_failed", error=str(e))

def background_http_call(url: str, payload: dict):
    # Run async function in a new event loop
    asyncio.run(make_async_request(url, payload))
```

### Webhook Pattern for Background Tasks
```python
import httpx
from urllib.parse import urlparse

async def send_webhook_notification(webhook_url: str, payload: dict):
    parsed = urlparse(webhook_url)
    if not parsed.scheme or not parsed.netloc:
        logger.error("invalid_webhook_url", url=webhook_url)
        return False

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.post(webhook_url, json=payload)
            response.raise_for_status()
            logger.info("webhook_sent_successfully", url=webhook_url)
            return True
        except httpx.HTTPStatusError as e:
            logger.error("webhook_failed",
                        status_code=e.response.status_code,
                        url=webhook_url)
            return False
        except httpx.RequestError as e:
            logger.error("webhook_request_failed",
                        error=str(e),
                        url=webhook_url)
            return False

def background_task_with_webhook(task_id: str, webhook_url: str, data: dict):
    try:
        result = process_task(data)
        # Send webhook notification
        webhook_payload = {
            "task_id": task_id,
            "status": "completed",
            "result": result,
            "timestamp": datetime.utcnow().isoformat()
        }
        asyncio.run(send_webhook_notification(webhook_url, webhook_payload))
    except Exception as e:
        # Send failure notification
        error_payload = {
            "task_id": task_id,
            "status": "failed",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }
        asyncio.run(send_webhook_notification(webhook_url, error_payload))
        raise  # Re-raise to ensure error is logged in main handler
```

## Approved Code Pattern (From Specification)

### The Complete Pattern
```python
import structlog
from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db_session

logger = structlog.get_logger()
router = APIRouter()

# ---------------------------------------------------------
# 1. THE ISOLATED TASK FUNCTION
# ---------------------------------------------------------
async def _task_process_upload(file_id: str, org_id: str):
    """
    Independent logic function.
    Manages its own error handling and DB session.
    """
    log = logger.bind(task="process_upload", file_id=file_id)

    try:
        log.info("task_started")

        # Create NEW DB session here (Do not reuse route session)
        async with get_db_session() as db:
            # ... Perform heavy logic, DB updates, etc ...
            await db.commit()

        log.info("task_completed")

    except Exception as e:
        # Catch ALL errors to prevent worker crash
        log.exception("task_failed_critical", error=str(e))

# ---------------------------------------------------------
# 2. THE API ENDPOINT
# ---------------------------------------------------------
@router.post("/import-contacts", status_code=202)
async def import_contacts(
    file_id: str,
    background_tasks: BackgroundTasks,  # <--- Inject Native Runner
    current_user = Depends(get_current_user)
):
    """
    Returns immediately, processes in background.
    """
    logger.info("scheduling_import", user=current_user.id)

    # Schedule the task
    background_tasks.add_task(
        _task_process_upload,
        file_id=file_id,
        org_id=current_user.org_id
    )

    return {
        "status": "accepted",
        "message": "Import started. You will be notified upon completion."
    }
```

## Task Retry Patterns

### Exponential Backoff with Retry Logic
```python
import random
import asyncio
from typing import Type, Tuple

def retry_async(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    backoff_factor: float = 2.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,)
):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e

                    if attempt == max_retries:
                        logger.error(
                            "task_failed_after_maximum_retries",
                            attempts=max_retries + 1,
                            error=str(e)
                        )
                        raise e

                    delay = min(
                        base_delay * (backoff_factor ** attempt) + random.uniform(0, 1),
                        max_delay
                    )

                    logger.warning(
                        "task_attempt_failed_retrying",
                        attempt=attempt + 1,
                        delay=delay,
                        error=str(e)
                    )
                    await asyncio.sleep(delay)

            raise last_exception
        return wrapper
    return decorator

@retry_async(max_retries=3, exceptions=(ConnectionError, TimeoutError))
async def resilient_background_task(url: str, data: dict):
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(url, json=data)
        response.raise_for_status()
        return response.json()
```

## Native FastAPI Capabilities vs External Message Brokers

### FastAPI BackgroundTasks
- **Pros**: Built-in, simple, no extra infrastructure, lightweight
- **Cons**: In-memory, no persistence, limited scalability, no monitoring
- **Best for**: Simple, quick tasks that don't require reliability

### Forbidden Technologies (Per Specification)
- ❌ Celery: Adds Redis/RabbitMQ infrastructure complexity
- ❌ Redis: Not allowed for this monolithic, low-latency MVP
- ❌ RabbitMQ: Overcomplicates simple background tasks
- ❌ Kafka: Overkill for simple fire-and-forget tasks

### When to Use BackgroundTasks
- Email notifications
- File processing
- Webhook deliveries
- Data exports
- Simple report generation
- Cache warming
- Any task that doesn't require guaranteed delivery

### When to Consider Alternatives (Future)
- Mission-critical tasks requiring guaranteed delivery
- Long-running computations (> few minutes)
- High-volume task processing
- Complex task orchestration
- Advanced monitoring and retry requirements

## Performance Optimization Guidelines

### Keep Tasks Lightweight
- Process tasks quickly (under 30 seconds if possible)
- Avoid heavy computations in background
- Use efficient database queries
- Implement proper error handling to prevent hanging tasks

### Monitor Task Performance
- Log task start/end times
- Track execution durations
- Monitor for hanging tasks
- Implement timeouts where appropriate

### Resource Management
- Limit concurrent background tasks if needed
- Use semaphores for resource-intensive operations
- Properly close database connections
- Clean up temporary resources