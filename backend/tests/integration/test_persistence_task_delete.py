import pytest
import uuid
from api.database.session import get_db_session
from api.database.repositories.task_repository import TaskRepository

@pytest.mark.asyncio
async def test_soft_delete_task():
    async for session in get_db_session():
        repo = TaskRepository(session)
        user_id = str(uuid.uuid4())
        
        task = await repo.create_task(user_id, {"title": "To Delete"})
        await repo.soft_delete_task(user_id, task.id)
        
        tasks = await repo.get_active_tasks(user_id)
        assert len(tasks) == 0
        
        # Cleanup (hard delete)
        await session.delete(task)
        await session.commit()
        return
