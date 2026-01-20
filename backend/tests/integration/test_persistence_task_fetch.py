import pytest
import uuid
from api.database.session import get_db_session
from api.database.repositories.task_repository import TaskRepository

@pytest.mark.asyncio
async def test_fetch_active_tasks():
    async for session in get_db_session():
        repo = TaskRepository(session)
        user_id = str(uuid.uuid4())
        
        t1 = await repo.create_task(user_id, {"title": "Task 1"})
        t2 = await repo.create_task(user_id, {"title": "Task 2"})
        
        tasks = await repo.get_active_tasks(user_id)
        assert len(tasks) == 2
        
        # Cleanup
        await session.delete(t1)
        await session.delete(t2)
        await session.commit()
        return
