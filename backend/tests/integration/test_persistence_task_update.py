import pytest
import uuid
from api.database.session import get_db_session
from api.database.repositories.task_repository import TaskRepository

@pytest.mark.asyncio
async def test_update_task():
    async for session in get_db_session():
        repo = TaskRepository(session)
        user_id = str(uuid.uuid4())
        
        task = await repo.create_task(user_id, {"title": "Original"})
        updated = await repo.update_task(user_id, task.id, {"title": "Updated"})
        
        assert updated.title == "Updated"
        
        # Cleanup
        await session.delete(task)
        await session.commit()
        return
