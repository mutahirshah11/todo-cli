import asyncio
import uuid
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.database.session import get_db_session
from api.database.repositories.task_repository import TaskRepository

async def main():
    print("Connecting to DB...")
    async for session in get_db_session():
        print("Connected.")
        repo = TaskRepository(session)
        user_id = str(uuid.uuid4())
        task_data = {"title": "Script Test Task"}
        
        print(f"Creating task for user {user_id}...")
        task = await repo.create_task(user_id, task_data)
        
        print(f"Task created: {task.id} - {task.title}")
        assert task.id is not None
        assert task.title == "Script Test Task"
        
        print("Cleaning up...")
        await session.delete(task)
        await session.commit()
        print("Deleted.")
        return

if __name__ == "__main__":
    try:
        if sys.platform == 'win32':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(main())
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
