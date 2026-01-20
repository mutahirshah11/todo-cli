import pytest
import uuid
from api.database.session import get_db_session
from api.database.repositories.task_repository import TaskRepository
from api.database.models.task import Task

@pytest.mark.asyncio
async def test_create_task_persistence():
    async for session in get_db_session():
        repo = TaskRepository(session)
        user_id = str(uuid.uuid4())
        task_data = {"title": "Integration Test Task"}
        
        # Create
        task = await repo.create_task(user_id, task_data)
        
        assert task.id is not None
        assert task.user_id == user_id
        assert task.title == "Integration Test Task"
        assert task.deleted_at is None
        
        # Cleanup
        await session.delete(task)
        await session.commit()
        return