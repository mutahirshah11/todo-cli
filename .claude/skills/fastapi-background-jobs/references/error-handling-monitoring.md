# Error Handling and Monitoring in FastAPI Background Tasks

## The Silent Failure Problem

### Why Background Task Failures Are Silent
Background tasks in FastAPI execute after the HTTP response is sent to the client. If a background task fails:

- The user receives no indication of failure
- The server may log a stack trace, but it's often buried in logs
- Errors can go unnoticed, leading to data inconsistency
- Without proper monitoring, failures accumulate silently

### The Critical Need for Error Handling
```python
# ❌ WRONG - Silent failure
def bad_background_task(item_id: int):
    # If this fails, user never knows
    result = process_heavy_computation(item_id)
    update_database(result)  # Might fail, but nobody knows!

# ✅ RIGHT - Proper error handling
def good_background_task(item_id: int):
    try:
        result = process_heavy_computation(item_id)
        update_database(result)
        logger.info("task_completed_successfully", item_id=item_id)
    except Exception as e:
        logger.exception("task_failed", item_id=item_id, error=str(e))
        # Optionally, implement error recovery or notification
```

## Comprehensive Error Handling Patterns

### Pattern 1: Comprehensive Try-Catch with Logging
```python
import traceback
from typing import Optional
import structlog

logger = structlog.get_logger()

def robust_background_task(task_data: dict) -> Optional[bool]:
    """Robust background task with comprehensive error handling."""
    task_id = task_data.get("task_id", "unknown")
    log = logger.bind(task_id=task_id)

    try:
        log.info("task_started", data=task_data)

        # Validate inputs
        if not task_data:
            log.warning("empty_task_data_received")
            return False

        # Perform main task logic
        result = process_task_logic(task_data)

        log.info("task_completed_successfully", result=result)
        return True

    except ValueError as ve:
        log.error("invalid_input_data", error=str(ve))
        return False
    except ConnectionError as ce:
        log.error("connection_failed", error=str(ce))
        # Could implement retry logic here
        return False
    except Exception as e:
        log.error("unexpected_error_in_background_task",
                 error=str(e),
                 traceback=traceback.format_exc())
        return False
```

### Pattern 2: Error Classification and Handling
```python
from enum import Enum
from typing import NamedTuple

class ErrorType(Enum):
    VALIDATION_ERROR = "validation_error"
    CONNECTION_ERROR = "connection_error"
    BUSINESS_ERROR = "business_error"
    SYSTEM_ERROR = "system_error"
    UNKNOWN_ERROR = "unknown_error"

class TaskResult(NamedTuple):
    success: bool
    error_type: ErrorType
    error_message: str

def classified_background_task(task_data: dict) -> TaskResult:
    """Background task with classified error handling."""
    try:
        # Validate input
        if not task_data:
            return TaskResult(False, ErrorType.VALIDATION_ERROR, "Empty task data")

        # Process task
        result = process_task_logic(task_data)

        logger.info("task_completed", result=result)
        return TaskResult(True, ErrorType.UNKNOWN_ERROR, "")  # Success case

    except ValueError as e:
        error_msg = f"Validation error: {str(e)}"
        logger.error("task_validation_error", error=error_msg)
        return TaskResult(False, ErrorType.VALIDATION_ERROR, error_msg)

    except ConnectionError as e:
        error_msg = f"Connection error: {str(e)}"
        logger.error("task_connection_error", error=error_msg)
        return TaskResult(False, ErrorType.CONNECTION_ERROR, error_msg)

    except BusinessRuleViolation as e:
        error_msg = f"Business rule violation: {str(e)}"
        logger.error("task_business_error", error=error_msg)
        return TaskResult(False, ErrorType.BUSINESS_ERROR, error_msg)

    except Exception as e:
        error_msg = f"System error: {str(e)}"
        logger.error("task_system_error", error=error_msg, traceback=traceback.format_exc())
        return TaskResult(False, ErrorType.SYSTEM_ERROR, error_msg)
```

### Pattern 3: Circuit Breaker Pattern for Background Tasks
```python
import time
from enum import Enum
from typing import Optional

class CircuitState(Enum):
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Trip threshold exceeded
    HALF_OPEN = "half_open"  # Testing recovery

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED

    def call(self, func, *args, **kwargs):
        """Execute function with circuit breaker protection."""
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time >= self.timeout:
                self.state = CircuitState.HALF_OPEN
            else:
                raise Exception("Circuit breaker is OPEN")

        try:
            result = func(*args, **kwargs)
            self.on_success()
            return result
        except Exception as e:
            self.on_failure()
            raise e

    def on_success(self):
        """Called when operation succeeds."""
        self.failure_count = 0
        self.state = CircuitState.CLOSED

    def on_failure(self):
        """Called when operation fails."""
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN

# Global circuit breaker for background tasks
background_circuit_breaker = CircuitBreaker(failure_threshold=3, timeout=300)  # 5 min

def circuit_protected_background_task(task_data: dict):
    """Background task with circuit breaker protection."""
    def _execute_task():
        # Your actual task logic here
        return process_task_logic(task_data)

    try:
        result = background_circuit_breaker.call(_execute_task)
        logger.info("circuit_task_completed", success=True)
        return result
    except Exception as e:
        logger.error("circuit_task_failed", error=str(e))
        raise
```

## Advanced Error Recovery Patterns

### Pattern 4: Retry with Exponential Backoff
```python
import asyncio
import random
from typing import Callable, Type, Tuple, Any

def retry_with_backoff(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    backoff_factor: float = 2.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    jitter: bool = True
):
    """
    Decorator for retrying background tasks with exponential backoff.

    Args:
        max_retries: Maximum number of retry attempts
        base_delay: Initial delay between retries (seconds)
        max_delay: Maximum delay between retries (seconds)
        backoff_factor: Factor by which delay increases after each retry
        exceptions: Tuple of exception types to retry on
        jitter: Whether to add random jitter to delays
    """
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e

                    if attempt == max_retries:
                        logger.error(
                            "task_failed_after_max_retries",
                            function=func.__name__,
                            attempts=max_retries + 1,
                            error=str(e),
                            traceback=traceback.format_exc()
                        )
                        raise e

                    # Calculate delay with exponential backoff
                    delay = min(
                        base_delay * (backoff_factor ** attempt),
                        max_delay
                    )

                    # Add jitter to prevent thundering herd
                    if jitter:
                        delay = delay * random.uniform(0.5, 1.5)

                    logger.warning(
                        "task_attempt_failed_retrying",
                        function=func.__name__,
                        attempt=attempt + 1,
                        max_attempts=max_retries + 1,
                        delay=round(delay, 2),
                        error=str(e)
                    )

                    time.sleep(delay)

            raise last_exception
        return wrapper
    return decorator

@retry_with_backoff(
    max_retries=3,
    base_delay=1.0,
    exceptions=(ConnectionError, TimeoutError, DatabaseError)
)
def resilient_background_task(url: str, payload: dict):
    """Background task with built-in retry logic."""
    # Your task logic here
    return make_http_request(url, payload)
```

### Pattern 5: Dead Letter Queue Pattern
```python
from datetime import datetime, timedelta
from typing import Dict, Any

class DeadLetterQueue:
    """Manages failed background tasks for later inspection."""

    def __init__(self, max_retries: int = 5):
        self.max_retries = max_retries
        self.failed_tasks = []

    def add_failed_task(self, task_name: str, task_data: Dict[str, Any], error: Exception):
        """Add a failed task to the dead letter queue."""
        failed_task = {
            "task_name": task_name,
            "task_data": task_data,
            "error": str(error),
            "timestamp": datetime.utcnow(),
            "attempt_count": 1,
            "last_error": str(error)
        }
        self.failed_tasks.append(failed_task)
        logger.warning("task_moved_to_dead_letter_queue",
                      task_name=task_name, error=str(error))

    def should_retry(self, failed_task: Dict[str, Any]) -> bool:
        """Determine if a failed task should be retried."""
        return failed_task["attempt_count"] < self.max_retries

    def get_retryable_tasks(self) -> list:
        """Get tasks that should be retried."""
        return [task for task in self.failed_tasks if self.should_retry(task)]

# Global dead letter queue
dlq = DeadLetterQueue(max_retries=3)

def background_task_with_dlq(task_name: str, task_data: dict):
    """Background task with dead letter queue support."""
    try:
        # Execute the actual task
        result = execute_task(task_name, task_data)
        logger.info("task_completed_successfully", task_name=task_name)
        return result

    except Exception as e:
        # Add to dead letter queue
        dlq.add_failed_task(task_name, task_data, e)

        # Optionally, try to handle specific error types
        if isinstance(e, PermanentError):
            logger.error("permanent_task_failure", task_name=task_name, error=str(e))
        else:
            logger.warning("temporary_task_failure_queued_for_retry",
                          task_name=task_name, error=str(e))

        raise  # Re-raise to ensure caller knows about the failure
```

## Monitoring and Observability

### Pattern 6: Comprehensive Task Monitoring
```python
import time
from contextlib import contextmanager
from prometheus_client import Counter, Histogram, Gauge

# Prometheus metrics
task_counter = Counter('background_tasks_total', 'Total background tasks', ['status', 'task_type'])
task_duration = Histogram('background_task_duration_seconds', 'Duration of background tasks', ['task_type'])
active_tasks = Gauge('background_tasks_active', 'Currently active background tasks', ['task_type'])

@contextmanager
def monitor_task(task_type: str, task_id: str = None):
    """Context manager for monitoring background task execution."""
    start_time = time.time()
    task_counter.labels(status='started', task_type=task_type).inc()
    active_tasks.labels(task_type=task_type).inc()

    log = logger.bind(task_type=task_type, task_id=task_id) if task_id else logger.bind(task_type=task_type)
    log.info("task_monitoring_started")

    try:
        yield log
        task_counter.labels(status='success', task_type=task_type).inc()
        log.info("task_monitoring_success")
    except Exception as e:
        task_counter.labels(status='error', task_type=task_type).inc()
        log.error("task_monitoring_error", error=str(e))
        raise
    finally:
        duration = time.time() - start_time
        task_duration.labels(task_type=task_type).observe(duration)
        active_tasks.labels(task_type=task_type).dec()
        log.info("task_monitoring_completed", duration=round(duration, 2))

def monitored_background_task(task_type: str, task_id: str, task_data: dict):
    """Background task with comprehensive monitoring."""
    with monitor_task(task_type, task_id) as log:
        log.info("processing_task", data=task_data)

        # Your actual task logic here
        result = process_task_logic(task_data)

        log.info("task_processing_complete", result=result)
        return result
```

### Pattern 7: Health Check and Task Status Tracking
```python
from datetime import datetime, timedelta
from typing import Dict, List
from enum import Enum

class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"

class TaskTracker:
    """Tracks background task status and health."""

    def __init__(self, timeout_seconds: int = 300):  # 5 minutes default timeout
        self.timeout_seconds = timeout_seconds
        self.task_registry = {}
        self.max_retained_tasks = 1000

    def register_task(self, task_id: str, task_type: str):
        """Register a new background task."""
        self.task_registry[task_id] = {
            "task_id": task_id,
            "task_type": task_type,
            "status": TaskStatus.RUNNING,
            "start_time": datetime.utcnow(),
            "errors": []
        }

        # Trim registry if too large
        if len(self.task_registry) > self.max_retained_tasks:
            self.cleanup_old_tasks()

    def complete_task(self, task_id: str, success: bool = True):
        """Mark a task as completed."""
        if task_id in self.task_registry:
            self.task_registry[task_id]["status"] = TaskStatus.COMPLETED if success else TaskStatus.FAILED
            self.task_registry[task_id]["end_time"] = datetime.utcnow()

    def add_error(self, task_id: str, error: str):
        """Add an error to a task."""
        if task_id in self.task_registry:
            self.task_registry[task_id]["errors"].append({
                "timestamp": datetime.utcnow(),
                "error": error
            })

    def get_health_report(self) -> Dict[str, Any]:
        """Get a health report of background tasks."""
        now = datetime.utcnow()
        report = {
            "timestamp": now.isoformat(),
            "total_tasks": len(self.task_registry),
            "running_tasks": 0,
            "failed_tasks": 0,
            "timed_out_tasks": 0,
            "recent_errors": []
        }

        for task_id, task_info in self.task_registry.items():
            age = (now - task_info["start_time"]).total_seconds()

            if task_info["status"] == TaskStatus.RUNNING:
                report["running_tasks"] += 1
                if age > self.timeout_seconds:
                    task_info["status"] = TaskStatus.TIMEOUT
                    report["timed_out_tasks"] += 1
            elif task_info["status"] == TaskStatus.FAILED:
                report["failed_tasks"] += 1

                # Collect recent errors
                if task_info["errors"]:
                    latest_error = task_info["errors"][-1]
                    report["recent_errors"].append({
                        "task_id": task_id,
                        "error": latest_error["error"],
                        "timestamp": latest_error["timestamp"].isoformat()
                    })

        return report

    def cleanup_old_tasks(self):
        """Clean up old completed tasks to prevent memory leaks."""
        now = datetime.utcnow()
        cutoff_time = now - timedelta(hours=24)  # Keep tasks for 24 hours

        old_tasks = [
            task_id for task_id, task_info in self.task_registry.items()
            if task_info.get("end_time", now) < cutoff_time
        ]

        for task_id in old_tasks:
            del self.task_registry[task_id]

# Global task tracker
task_tracker = TaskTracker(timeout_seconds=300)

def tracked_background_task(task_type: str, task_data: dict) -> str:
    """Background task with tracking."""
    task_id = str(uuid.uuid4())

    # Register the task
    task_tracker.register_task(task_id, task_type)
    log = logger.bind(task_id=task_id, task_type=task_type)

    try:
        log.info("tracked_task_started", data=task_data)

        # Execute task logic
        result = process_task_logic(task_data)

        # Mark as completed
        task_tracker.complete_task(task_id, success=True)
        log.info("tracked_task_completed", result=result)

        return result

    except Exception as e:
        # Mark as failed and add error
        task_tracker.complete_task(task_id, success=False)
        task_tracker.add_error(task_id, str(e))

        log.error("tracked_task_failed", error=str(e))
        raise
```

## Error Notification and Alerting

### Pattern 8: Error Notification System
```python
import asyncio
from typing import List, Dict, Any
from abc import ABC, abstractmethod

class NotificationTarget(ABC):
    """Abstract base class for notification targets."""

    @abstractmethod
    async def send_notification(self, message: str, details: Dict[str, Any]):
        """Send notification to the target."""
        pass

class SlackNotification(NotificationTarget):
    """Slack notification target."""

    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    async def send_notification(self, message: str, details: Dict[str, Any]):
        import httpx

        payload = {
            "text": message,
            "attachments": [{
                "fields": [
                    {"title": key, "value": str(value), "short": True}
                    for key, value in details.items()
                ]
            }]
        }

        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                await client.post(self.webhook_url, json=payload)
            except Exception as e:
                logger.error("slack_notification_failed", error=str(e))

class EmailNotification(NotificationTarget):
    """Email notification target."""

    def __init__(self, smtp_config: Dict[str, Any]):
        self.smtp_config = smtp_config

    async def send_notification(self, message: str, details: Dict[str, Any]):
        # Implementation for sending email notifications
        pass

class ErrorNotificationSystem:
    """System for sending notifications about background task errors."""

    def __init__(self):
        self.targets: List[NotificationTarget] = []
        self.severity_threshold = 5  # Send alerts after this many consecutive errors

    def add_target(self, target: NotificationTarget):
        """Add a notification target."""
        self.targets.append(target)

    def should_alert(self, task_type: str, error_count: int) -> bool:
        """Determine if an alert should be sent."""
        return error_count >= self.severity_threshold

    async def notify_error(self, task_type: str, task_id: str, error: str):
        """Send error notification to all targets."""
        error_details = {
            "task_type": task_type,
            "task_id": task_id,
            "error": error,
            "timestamp": datetime.utcnow().isoformat()
        }

        message = f"❌ Background Task Failed: {task_type} ({task_id})"

        # Send to all targets concurrently
        tasks = [
            target.send_notification(message, error_details)
            for target in self.targets
        ]

        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

# Global notification system
notification_system = ErrorNotificationSystem()

# Add notification targets
# notification_system.add_target(SlackNotification(os.getenv("SLACK_WEBHOOK_URL")))

def background_task_with_notifications(task_type: str, task_data: dict):
    """Background task with error notifications."""
    task_id = str(uuid.uuid4())
    log = logger.bind(task_id=task_id, task_type=task_type)

    try:
        log.info("task_with_notifications_started", data=task_data)

        result = process_task_logic(task_data)

        log.info("task_with_notifications_completed", result=result)
        return result

    except Exception as e:
        # Send notification about the error
        asyncio.create_task(
            notification_system.notify_error(task_type, task_id, str(e))
        )

        log.error("task_with_notifications_failed", error=str(e))
        raise
```

## Best Practices Summary

### 1. Always Wrap in Try-Catch
- Every background task must have comprehensive error handling
- Log all exceptions with context
- Don't let exceptions bubble up silently

### 2. Use Structured Logging
- Include task identifiers in all log messages
- Log task start, progress, and completion
- Include relevant context with each log message

### 3. Implement Retry Logic
- Use exponential backoff for transient failures
- Distinguish between retryable and permanent errors
- Set reasonable retry limits

### 4. Monitor Task Health
- Track task success/failure rates
- Monitor execution times
- Set up alerts for unusual patterns

### 5. Plan for Error Recovery
- Implement dead letter queues for failed tasks
- Provide manual recovery mechanisms
- Document error scenarios and recovery procedures

### 6. Test Error Scenarios
- Test how your application behaves with failing background tasks
- Verify that errors are properly logged and monitored
- Ensure that failing tasks don't impact the main application flow

By following these patterns and best practices, you can build robust background task systems that handle errors gracefully and provide visibility into their operation.