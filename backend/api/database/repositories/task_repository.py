from typing import List, Optional
from uuid import UUID
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from api.database.models.task import Task, TaskStatus
from datetime import datetime, timezone

class TaskRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_task(self, user_id: str, data: dict) -> Task:
        # data should be validated before passing here, or we trust Pydantic model
        task = Task(**data)
        task.user_id = user_id
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return task
    
    async def get_active_tasks(self, user_id: str) -> List[Task]:
        statement = select(Task).where(
            Task.user_id == user_id,
            Task.deleted_at == None
        )
        result = await self.session.execute(statement)
        return result.scalars().all()

    async def update_task(self, user_id: str, task_id: UUID, data: dict) -> Optional[Task]:
        statement = select(Task).where(
            Task.id == task_id,
            Task.user_id == user_id
        )
        result = await self.session.execute(statement)
        task = result.scalars().first()
        if not task:
            return None
            
        for key, value in data.items():
            if hasattr(task, key):
                setattr(task, key, value)
        
        task.updated_at = datetime.now(timezone.utc)
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def soft_delete_task(self, user_id: str, task_id: UUID) -> bool:
        statement = select(Task).where(
            Task.id == task_id,
            Task.user_id == user_id
        )
        result = await self.session.execute(statement)
        task = result.scalars().first()
        if not task:
            return False
            
        task.deleted_at = datetime.now(timezone.utc)
        self.session.add(task)
        await self.session.commit()
        return True
