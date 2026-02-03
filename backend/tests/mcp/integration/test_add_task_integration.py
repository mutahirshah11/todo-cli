import pytest
from uuid import uuid4
from api.mcp.tools import add_task_tool
from api.database.session import AsyncSessionLocal
from sqlalchemy import text
from sqlmodel import select
from api.models.database import Task

@pytest.mark.asyncio
async def test_add_task_integration():
    """Test add_task tool against a real database."""
    user_id = str(uuid4())
    title = f"Integration Test Task {uuid4()}"
    description = "Created via MCP Integration Test"

    # 1. Call the tool
    result_json = await add_task_tool(user_id=user_id, title=title, description=description)

    # 2. Verify result contains expected data
    assert title in result_json
    assert "id" in result_json

    # 3. Verify task exists in database
    async with AsyncSessionLocal() as session:
        statement = select(Task).where(Task.title == title, Task.user_id == user_id)
        result = await session.execute(statement)
        task = result.scalar_one_or_none()
        
        assert task is not None
        assert task.title == title
        assert task.description == description
        assert task.user_id == user_id
        assert task.is_completed is False
        
        # Cleanup
        await session.delete(task)
        await session.commit()
