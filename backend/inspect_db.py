import asyncio
import os
from dotenv import load_dotenv
from sqlmodel import select
from api.database.session import AsyncSessionLocal
from api.models.database import Task

load_dotenv()

async def inspect_tasks():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Task))
        tasks = result.scalars().all()
        
        print(f"{'ID':<36} | {'Title':<20} | {'User ID':<36} | {'Status'}")
        print("-" * 110)
        for t in tasks:
            status = "Done" if t.is_completed else "Pending"
            print(f"{str(t.id):<36} | {t.title:<20} | {t.user_id:<36} | {status}")

if __name__ == "__main__":
    asyncio.run(inspect_tasks())
