from sqlmodel import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
import os
import asyncio
from typing import AsyncGenerator
from urllib.parse import urlparse


# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/neondb?sslmode=require")

# Parse the database URL to customize connection parameters for Neon
parsed_url = urlparse(DATABASE_URL)

# Async engine for FastAPI with Neon-specific configuration
# Ensure DATABASE_URL uses async driver (e.g., postgresql+asyncpg:// instead of postgresql://)
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
elif DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)

async_engine = create_async_engine(
    DATABASE_URL,
    # Neon-specific connection pooling settings for async engines
    pool_size=5,  # Smaller pool size for serverless
    max_overflow=10,  # Allow some overflow during peak loads
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=3600,  # Recycle connections every hour
    echo=False,  # Set to True for SQL query logging
)

# Async session maker for dependency injection
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency generator for FastAPI to provide database sessions.
    Ensures proper session lifecycle management with automatic cleanup.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def test_connection():
    """
    Test function to verify database connection works properly.
    """
    try:
        async with AsyncSessionLocal() as session:
            # Execute a simple query to test connection
            result = await session.execute("SELECT 1")
            print("Database connection successful!")
            return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False


# Connection retry mechanism
async def get_db_session_with_retry(max_retries: int = 3, delay: float = 1.0):
    """
    Get database session with retry mechanism for handling temporary connection failures.
    """
    for attempt in range(max_retries):
        try:
            async with AsyncSessionLocal() as session:
                # Test the connection
                await session.execute("SELECT 1")
                yield session
                return
        except Exception as e:
            if attempt == max_retries - 1:
                # Last attempt - raise the exception
                raise e
            # Wait before retrying
            await asyncio.sleep(delay * (2 ** attempt))  # Exponential backoff


class DatabaseErrorHandler:
    """
    A utility class to handle database errors with retry mechanisms and logging.
    """

    @staticmethod
    async def execute_with_retry(func, max_retries: int = 3, delay: float = 1.0, exponential_backoff: bool = True):
        """
        Execute a database operation with retry mechanism.

        Args:
            func: The async function to execute
            max_retries: Maximum number of retry attempts
            delay: Initial delay between retries (seconds)
            exponential_backoff: Whether to use exponential backoff for delays

        Returns:
            Result of the function call

        Raises:
            Exception: If all retry attempts fail
        """
        last_exception = None

        for attempt in range(max_retries):
            try:
                return await func()
            except Exception as e:
                last_exception = e

                if attempt == max_retries - 1:
                    # This was the last attempt
                    break

                # Calculate delay with optional exponential backoff
                current_delay = delay * (2 ** attempt) if exponential_backoff else delay
                print(f"Database operation failed (attempt {attempt + 1}/{max_retries}): {e}. Retrying in {current_delay}s...")

                # Wait before retrying
                await asyncio.sleep(current_delay)

        # If we get here, all attempts failed
        raise last_exception

    @staticmethod
    def handle_database_error(error: Exception, operation: str = "database operation"):
        """
        Log and handle database errors appropriately.

        Args:
            error: The exception that occurred
            operation: Description of the operation that failed
        """
        import logging
        logger = logging.getLogger(__name__)

        logger.error(f"{operation} failed: {str(error)}")

        # Different handling based on error type
        if "connection" in str(error).lower() or "timeout" in str(error).lower():
            logger.warning("Connection-related error detected - consider retrying with backoff")
        elif "constraint" in str(error).lower():
            logger.warning("Constraint violation - check data integrity")
        else:
            logger.error(f"Unexpected database error: {str(error)}")


# Enhanced session generator with error handling
async def get_db_session_with_error_handling():
    """
    Get database session with comprehensive error handling.
    """
    try:
        async with AsyncSessionLocal() as session:
            try:
                # Test connection before yielding
                await session.execute("SELECT 1")
                yield session
            except Exception as e:
                DatabaseErrorHandler.handle_database_error(e, "Session creation")
                raise
    except Exception as e:
        DatabaseErrorHandler.handle_database_error(e, "Database session acquisition")
        raise


# Timeout handling decorator
def with_timeout(seconds: int):
    """
    Decorator to add timeout handling to database operations.

    Args:
        seconds: Number of seconds before timeout
    """
    def decorator(func):
        async def wrapper(*args, **kwargs):
            try:
                return await asyncio.wait_for(func(*args, **kwargs), timeout=seconds)
            except asyncio.TimeoutError:
                raise Exception(f"Operation timed out after {seconds} seconds")
        return wrapper
    return decorator