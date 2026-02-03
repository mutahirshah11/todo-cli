from api.database.session import AsyncSessionLocal
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Any, Dict
from sqlalchemy.ext.asyncio import AsyncSession
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def get_mcp_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Async context manager for MCP tools to get a database session.
    Ensures session is closed after use.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"Database error in MCP tool: {str(e)}")
            raise
        finally:
            await session.close()

def format_error_response(error_message: str) -> str:
    """Formats an error message as a simple string for the agent."""
    return f"Error: {error_message}"

def format_success_response(data: Dict[str, Any]) -> str:
    """Formats a success response (dictionary) as a string representation."""
    import json
    # Use json.dumps to ensure it's a valid string representation of the data
    try:
        return json.dumps(data, default=str)
    except Exception as e:
        return f"Success (formatting failed): {str(data)}"