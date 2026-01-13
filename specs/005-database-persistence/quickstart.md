# Quickstart Guide: Database Integration for Todo Full-Stack Web Application

## Prerequisites

### Neon PostgreSQL Setup
1. Create a Neon account at https://neon.tech/
2. Create a new project with the following settings:
   - Region: Choose closest to your users
   - PostgreSQL version: 15+
   - Branch: Default main branch
3. Note the connection string from the project dashboard

### Environment Configuration
Create a `.env` file in the backend directory with:
```bash
DATABASE_URL="postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/neondb?sslmode=require"
SECRET_KEY="your-jwt-secret-key-matching-auth-service"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

## Development Setup

### 1. Install Dependencies
```bash
# In the backend directory
pip install sqlmodel asyncpg alembic
```

### 2. Database Models Setup
Create the SQLModel database models:
```python
# In backend/api/models/database.py
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid

class User(SQLModel, table=True):
    user_id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    email: str = Field(unique=True, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)

class Task(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    title: str = Field(max_length=255)
    description: Optional[str] = Field(default=None)
    is_completed: bool = Field(default=False)
    user_id: str = Field(index=True, foreign_key="user.user_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### 3. Database Session Management
```python
# In backend/api/database/session.py
from sqlmodel import create_engine, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL")

# Async engine for FastAPI
async_engine = create_async_engine(DATABASE_URL)

# Async session maker
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Dependency for FastAPI
async def get_db_session():
    async with AsyncSessionLocal() as session:
        yield session
```

### 4. Repository Layer
```python
# In backend/api/repositories/task_repository.py
from typing import List, Optional
from sqlmodel import select
from sqlalchemy.exc import IntegrityError
from backend.api.models.database import Task, User
from backend.api.schemas.task import TaskCreate, TaskUpdate

class TaskRepository:
    def __init__(self, session):
        self.session = session

    async def get_tasks_by_user(self, user_id: str) -> List[Task]:
        statement = select(Task).where(Task.user_id == user_id)
        result = await self.session.execute(statement)
        return result.scalars().all()

    async def get_task_by_id(self, task_id: str, user_id: str) -> Optional[Task]:
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def create_task(self, task_create: TaskCreate, user_id: str) -> Task:
        db_task = Task(
            title=task_create.title,
            description=task_create.description,
            user_id=user_id
        )
        self.session.add(db_task)
        await self.session.commit()
        await self.session.refresh(db_task)
        return db_task

    async def update_task(self, task_id: str, task_update: TaskUpdate, user_id: str) -> Optional[Task]:
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = await self.session.execute(statement)
        db_task = result.scalar_one_or_none()

        if not db_task:
            return None

        # Update fields
        if task_update.title is not None:
            db_task.title = task_update.title
        if task_update.description is not None:
            db_task.description = task_update.description
        if task_update.completed is not None:
            db_task.is_completed = task_update.completed

        db_task.updated_at = datetime.utcnow()
        await self.session.commit()
        await self.session.refresh(db_task)
        return db_task

    async def delete_task(self, task_id: str, user_id: str) -> bool:
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = await self.session.execute(statement)
        db_task = result.scalar_one_or_none()

        if not db_task:
            return False

        await self.session.delete(db_task)
        await self.session.commit()
        return True
```

## Running the Application

### 1. Database Migration
```bash
# Run from backend directory
alembic init alembic
# Configure alembic.ini with your DATABASE_URL
alembic revision --autogenerate -m "Initial database schema"
alembic upgrade head
```

### 2. Start the Services
```bash
# Terminal 1: Start the auth service
cd auth
python start_auth_service.py --port 8002

# Terminal 2: Start the backend with database
cd backend
python -m uvicorn main:app --reload --port 8000

# Terminal 3: Start the frontend
cd frontend
npm run dev
```

## Testing the Integration

### 1. Verify Database Connection
```bash
# Check if the backend can connect to the database
curl -X GET http://localhost:8000/health
```

### 2. Test Authentication Flow
```bash
# Register a new user
curl -X POST http://localhost:8002/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"SecurePass123!"}'

# Login to get JWT token
curl -X POST http://localhost:8002/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"SecurePass123!"}'
```

### 3. Test Task Operations
```bash
# Replace YOUR_JWT_TOKEN with the token from login
# Create a task
curl -X POST http://localhost:8000/api/v1/user-uuid/tasks \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Task","description":"Test Description","completed":false}'

# Get all tasks
curl -X GET http://localhost:8000/api/v1/user-uuid/tasks \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Troubleshooting

### Common Issues
1. **Database Connection Errors**: Verify DATABASE_URL in .env file
2. **JWT Validation Errors**: Ensure SECRET_KEY matches the auth service
3. **User Access Errors**: Verify that the user_id in JWT matches the path parameter

### Health Checks
- Database connectivity: `SELECT 1;` query
- Authentication service: `/health` endpoint on auth service
- Backend service: `/health` endpoint on backend