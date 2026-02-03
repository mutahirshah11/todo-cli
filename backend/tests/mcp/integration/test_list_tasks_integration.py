import pytest
from uuid import uuid4
from api.mcp.tools import add_task_tool, list_tasks_tool
from api.database.session import AsyncSessionLocal
from sqlalchemy import text
from sqlmodel import select
from api.models.database import Task
from api.services.task_adapter import TaskAdapter
from api.models.task import TaskToggle

@pytest.mark.asyncio
async def test_list_tasks_integration():
    """Test list_tasks tool against a real database."""
    user_id = str(uuid4())
    title_1 = f"Task 1 {uuid4()}"
    title_2 = f"Task 2 {uuid4()}"

    # 1. Create tasks via tool
    await add_task_tool(user_id=user_id, title=title_1)
    await add_task_tool(user_id=user_id, title=title_2)

    # 2. List tasks
    result_json = await list_tasks_tool(user_id=user_id)

    # 3. Verify
    assert title_1 in result_json
    assert title_2 in result_json
    assert "tasks" in result_json
    
    # Cleanup
    async with AsyncSessionLocal() as session:
        statement = select(Task).where(Task.user_id == user_id)
        results = await session.execute(statement)
        tasks = results.scalars().all()
        for t in tasks:
            await session.delete(t)
        await session.commit()

@pytest.mark.asyncio
async def test_list_tasks_filter_integration():
    """Test list_tasks tool filtering."""
    user_id = str(uuid4())
    title_pending = f"Pending {uuid4()}"
    title_completed = f"Completed {uuid4()}"
    
    # Create tasks
    await add_task_tool(user_id=user_id, title=title_pending)
    await add_task_tool(user_id=user_id, title=title_completed)
    
    # Mark one as completed using Adapter directly (since we haven't implemented complete_task tool yet)
    async with AsyncSessionLocal() as session:
        # Find the task to complete
        statement = select(Task).where(Task.title == title_completed, Task.user_id == user_id)
        result = await session.execute(statement)
        task = result.scalar_one()
        
        adapter = TaskAdapter(session, user_id)
        await adapter.toggle_completion(str(task.id), TaskToggle(completed=True))

    # Test Filter Pending
    result_pending = await list_tasks_tool(user_id=user_id, status="pending")
    assert title_pending in result_pending
    assert title_completed not in result_pending
    
    # Test Filter Completed
    result_completed = await list_tasks_tool(user_id=user_id, status="completed")
    assert title_completed in result_completed
    assert title_pending not in result_completed
    
    # Cleanup
    async with AsyncSessionLocal() as session:
        statement = select(Task).where(Task.user_id == user_id)
        results = await session.execute(statement)
        tasks = results.scalars().all()
        for t in tasks:
            await session.delete(t)
        await session.commit()