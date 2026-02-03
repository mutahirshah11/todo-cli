import pytest
from uuid import uuid4
from api.mcp.tools import add_task_tool, update_task_tool, complete_task_tool, delete_task_tool, list_tasks_tool
from api.database.session import AsyncSessionLocal
from sqlalchemy import text
from sqlmodel import select
from api.models.database import Task
import json

@pytest.mark.asyncio
async def test_manage_tasks_lifecycle_integration():
    """Test full lifecycle: create -> update -> complete -> delete."""
    user_id = str(uuid4())
    title = f"Lifecycle Task {uuid4()}"
    
    # 1. Create
    res_create = await add_task_tool(user_id=user_id, title=title)
    task_data = json.loads(res_create)
    task_id = task_data['id']
    
    # 2. Update
    new_title = f"Updated {title}"
    res_update = await update_task_tool(user_id=user_id, task_id=task_id, title=new_title)
    assert new_title in res_update
    
    # 3. Complete
    res_complete = await complete_task_tool(user_id=user_id, task_id=task_id)
    assert "true" in res_complete.lower() # completed: true
    
    # 4. Verify in List
    res_list = await list_tasks_tool(user_id=user_id)
    assert new_title in res_list
    assert "true" in res_list.lower() # completed
    
    # 5. Delete
    res_delete = await delete_task_tool(user_id=user_id, task_id=task_id)
    assert "deleted" in res_delete
    
    # 6. Verify Gone
    res_list_after = await list_tasks_tool(user_id=user_id)
    assert new_title not in res_list_after
    
    # Cleanup (if delete failed?)
    async with AsyncSessionLocal() as session:
        statement = select(Task).where(Task.user_id == user_id)
        results = await session.execute(statement)
        tasks = results.scalars().all()
        for t in tasks:
            await session.delete(t)
        await session.commit()

@pytest.mark.asyncio
async def test_unauthorized_access_integration():
    """Test User A cannot modify User B's task."""
    user_a = str(uuid4())
    user_b = str(uuid4())
    
    # Create task for User A
    res_create = await add_task_tool(user_id=user_a, title="User A Task")
    task_data = json.loads(res_create)
    task_id = task_data['id']
    
    # User B tries to update
    res_update = await update_task_tool(user_id=user_b, task_id=task_id, title="Hacked")
    assert "Error" in res_update
    assert "unauthorized" in res_update.lower() or "not found" in res_update.lower()
    
    # User B tries to delete
    res_delete = await delete_task_tool(user_id=user_b, task_id=task_id)
    assert "Error" in res_delete
    
    # Cleanup
    async with AsyncSessionLocal() as session:
        statement = select(Task).where(Task.user_id == user_a)
        results = await session.execute(statement)
        tasks = results.scalars().all()
        for t in tasks:
            await session.delete(t)
        await session.commit()
