# Database Session Isolation in FastAPI Background Tasks

## The Critical Problem

### Why Session Isolation Matters
When working with background tasks in FastAPI, database session management becomes critical. The main request/response cycle closes database connections when the HTTP response is sent, but background tasks may continue running after this point. If you pass a database session from the main route to a background task, you'll encounter:

- `DetachedInstanceError` or `InvalidRequestError`
- Connection pool exhaustion
- Transaction inconsistencies
- Silent failures in background tasks

### The Session Lifecycle Issue
```python
# ❌ WRONG APPROACH - This will fail!
@app.post("/process-item/{item_id}")
async def process_item_wrong(
    item_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)  # Session from main request
):
    # The session will be closed when response is sent
    # Background task will fail when trying to use it
    background_tasks.add_task(process_item_in_background, item_id, db)
    return {"status": "processing_started"}

def process_item_in_background(item_id: int, db: Session):
    # This will fail! Session is closed.
    item = db.query(Item).filter(Item.id == item_id).first()  # ERROR!
```

## The Correct Approach

### Pattern 1: Create New Session in Background Task
```python
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Database setup
engine = create_engine("postgresql://user:pass@localhost/db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_db_session():
    """Context manager for database sessions."""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def process_item_in_background(item_id: int):
    """Background task that creates its own database session."""
    with get_db_session() as db:
        # Perform database operations with fresh session
        item = db.query(Item).filter(Item.id == item_id).first()
        if item:
            item.status = "processed"
            item.processed_at = datetime.utcnow()
            db.add(item)
        # Session is automatically committed and closed
```

### Pattern 2: Async Session Management
```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager

# Async database setup
async_engine = create_async_engine("postgresql+asyncpg://user:pass@localhost/db")
AsyncSessionLocal = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)

@asynccontextmanager
async def get_async_db_session():
    """Async context manager for database sessions."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

async def async_process_item_in_background(item_id: int):
    """Async background task with its own database session."""
    async with get_async_db_session() as db:
        # Use SQLAlchemy 2.0 async methods
        stmt = select(Item).where(Item.id == item_id)
        result = await db.execute(stmt)
        item = result.scalar_one_or_none()

        if item:
            item.status = "processed"
            item.processed_at = datetime.utcnow()
            db.add(item)
        # Session is automatically committed and closed
```

## Advanced Session Patterns

### Pattern 3: Session Factory Pattern
```python
from typing import Callable
from contextlib import contextmanager
from sqlalchemy.orm import Session

class DatabaseSessionFactory:
    """Factory for creating database sessions."""

    def __init__(self, engine):
        self.engine = engine
        self.sessionmaker = sessionmaker(bind=engine, expire_on_commit=False)

    @contextmanager
    def create_session(self) -> Session:
        """Create a new database session."""
        session = self.sessionmaker()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

# Global database factory
db_factory = DatabaseSessionFactory(engine)

def background_task_with_factory(item_id: int):
    """Background task using session factory."""
    with db_factory.create_session() as db:
        item = db.query(Item).filter(Item.id == item_id).first()
        # Process item...
```

### Pattern 4: Connection Pool Isolation
```python
from sqlalchemy.pool import QueuePool
import threading

class IsolatedConnectionPool:
    """Maintains separate connection pools for background tasks."""

    def __init__(self, database_url: str):
        self.database_url = database_url
        self.pools = {}

    def get_pool(self, task_type: str) -> QueuePool:
        """Get or create a connection pool for specific task type."""
        if task_type not in self.pools:
            # Create pool with specific settings for background tasks
            pool = QueuePool(
                creator=lambda: create_engine(self.database_url).connect(),
                pool_size=5,
                max_overflow=10,
                pre_ping=True
            )
            self.pools[task_type] = pool
        return self.pools[task_type]

    def get_connection(self, task_type: str):
        """Get connection from task-specific pool."""
        pool = self.get_pool(task_type)
        return pool.connect()

# Global connection pool manager
pool_manager = IsolatedConnectionPool("postgresql://user:pass@localhost/db")

def background_task_with_isolated_pool(item_id: int):
    """Background task with isolated connection pool."""
    connection = pool_manager.get_connection("item_processing")
    try:
        with Session(connection) as db:
            item = db.query(Item).filter(Item.id == item_id).first()
            # Process item...
    finally:
        connection.close()
```

## Common Session Isolation Scenarios

### Scenario 1: File Processing with Database Updates
```python
def process_uploaded_file(file_id: str, user_id: str):
    """Process uploaded file and update database."""
    log = logger.bind(task="file_processing", file_id=file_id)

    try:
        log.info("starting_file_processing")

        # Create new database session for background task
        with get_db_session() as db:
            # Get file record
            file_record = db.query(FileRecord).filter(FileRecord.id == file_id).first()
            if not file_record:
                log.error("file_not_found")
                return

            # Update status
            file_record.status = "processing"
            db.add(file_record)
            db.commit()

            # Process file
            processed_data = process_file_content(file_record.path)

            # Update with results
            file_record.status = "completed"
            file_record.processed_data = processed_data
            file_record.completed_at = datetime.utcnow()
            db.add(file_record)

        log.info("file_processing_completed")
    except Exception as e:
        log.exception("file_processing_failed", error=str(e))

        # Update error status (using a new session since previous one is closed)
        with get_db_session() as db:
            file_record = db.query(FileRecord).filter(FileRecord.id == file_id).first()
            if file_record:
                file_record.status = "failed"
                file_record.error_message = str(e)
                file_record.completed_at = datetime.utcnow()
                db.add(file_record)
```

### Scenario 2: Batch Processing with Multiple Records
```python
def batch_process_records(record_ids: list[str], operation_type: str):
    """Process multiple records in background."""
    log = logger.bind(task="batch_processing", operation_type=operation_type)

    try:
        log.info("starting_batch_processing", record_count=len(record_ids))

        processed_count = 0

        # Process in chunks to manage memory and connections
        chunk_size = 10
        for i in range(0, len(record_ids), chunk_size):
            chunk = record_ids[i:i + chunk_size]

            with get_db_session() as db:
                # Process chunk of records
                records = db.query(Record).filter(Record.id.in_(chunk)).all()

                for record in records:
                    try:
                        # Perform operation based on type
                        if operation_type == "validate":
                            result = validate_record(record)
                        elif operation_type == "transform":
                            result = transform_record(record)
                        else:
                            result = process_record(record)

                        record.status = "processed"
                        record.result = result
                        db.add(record)

                        processed_count += 1
                    except Exception as record_error:
                        log.error("record_processing_failed",
                                record_id=record.id,
                                error=str(record_error))
                        record.status = "failed"
                        record.error = str(record_error)
                        db.add(record)

                db.commit()  # Commit each chunk

        log.info("batch_processing_completed",
                processed_count=processed_count,
                total=len(record_ids))
    except Exception as e:
        log.exception("batch_processing_failed", error=str(e))
```

### Scenario 3: Event-Driven Processing
```python
def handle_domain_event(event_data: dict):
    """Handle domain event with database operations."""
    log = logger.bind(task="event_handling", event_type=event_data.get("type"))

    try:
        log.info("handling_domain_event", event_data=event_data)

        with get_db_session() as db:
            # Handle different event types
            event_type = event_data.get("type")

            if event_type == "user_registered":
                # Update user statistics
                stats = db.query(UserStats).filter(
                    UserStats.org_id == event_data["org_id"]
                ).first()

                if not stats:
                    stats = UserStats(org_id=event_data["org_id"], user_count=0)
                    db.add(stats)

                stats.user_count += 1
                stats.last_user_added = datetime.utcnow()

            elif event_type == "order_created":
                # Update inventory and order counts
                product_id = event_data["product_id"]
                quantity = event_data["quantity"]

                product = db.query(Product).filter(Product.id == product_id).first()
                if product:
                    product.inventory_count -= quantity
                    product.sales_count += 1

            db.commit()

        log.info("domain_event_handled")
    except Exception as e:
        log.exception("domain_event_handling_failed", error=str(e))
```

## Session Isolation Best Practices

### 1. Always Use Fresh Sessions
- Create a new session in each background task
- Never reuse sessions from the main request/response cycle
- Use context managers to ensure proper cleanup

### 2. Handle Transactions Properly
- Use explicit transaction management in background tasks
- Implement proper rollback on errors
- Commit frequently for long-running operations

### 3. Monitor Connection Usage
- Track connection pool usage for background tasks
- Set appropriate pool sizes for different task types
- Implement connection timeout and retry logic

### 4. Error Handling for Database Operations
- Wrap database operations in try/catch blocks
- Log database errors with context
- Implement retry logic for transient failures

### 5. Resource Cleanup
- Always close database sessions in finally blocks
- Use context managers for automatic cleanup
- Monitor for connection leaks in background tasks

## Performance Considerations

### Connection Pool Sizing
```python
# For background tasks, you might want different pool settings
BACKGROUND_POOL_SETTINGS = {
    "pool_size": 10,           # Smaller pool for background tasks
    "max_overflow": 20,        # Allow some overflow
    "pool_pre_ping": True,     # Verify connections before use
    "pool_recycle": 3600,      # Recycle connections hourly
    "pool_timeout": 30,        # Timeout after 30 seconds
}
```

### Batch Processing Optimization
```python
def optimized_batch_processing(records: list, batch_size: int = 100):
    """Optimized batch processing with proper session management."""
    total_processed = 0

    for i in range(0, len(records), batch_size):
        batch = records[i:i + batch_size]

        with get_db_session() as db:
            try:
                for record in batch:
                    process_single_record(db, record)

                db.commit()
                total_processed += len(batch)

                logger.info("batch_processed",
                           batch_start=i,
                           batch_size=len(batch),
                           total_processed=total_processed)
            except Exception as e:
                logger.error("batch_failed",
                           batch_start=i,
                           error=str(e))
                db.rollback()
                # Continue with next batch
                continue

    logger.info("all_batches_processed", total=total_processed)
```

## Common Pitfalls to Avoid

### 1. Passing Sessions Directly
```python
# ❌ DON'T DO THIS
@app.post("/process")
async def process_with_session(
    item_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    background_tasks.add_task(process_item, item_id, db)  # Wrong!

def process_item(item_id: int, db: Session):
    # Session is closed, will fail!
    pass
```

### 2. Reusing Connections
```python
# ❌ DON'T DO THIS
def bad_background_task(conn, item_id: int):
    # Connection may be closed or invalid
    cursor = conn.cursor()  # May fail!
```

### 3. Forgetting to Close Sessions
```python
# ❌ DON'T DO THIS
def leaky_background_task(item_id: int):
    db = SessionLocal()  # Created but never closed!
    item = db.query(Item).filter(Item.id == item_id).first()
    # db.close() never called - connection leaked!
```

### 4. Improper Error Handling
```python
# ❌ DON'T DO THIS
def dangerous_background_task(item_id: int):
    with get_db_session() as db:
        item = db.query(Item).filter(Item.id == item_id).first()
        item.status = "processing"
        db.add(item)
        # If exception occurs, transaction may be left in inconsistent state
        raise SomeException("Something went wrong")
        # db.commit() never reached!
```

By following these patterns and best practices, you can ensure that your background tasks properly manage database sessions without interfering with the main request/response cycle or causing connection issues.