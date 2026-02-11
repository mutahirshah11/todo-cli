# FastAPI Dependency Injection Patterns

## Basic Dependency Injection

### Simple Function Dependencies
```python
from fastapi import Depends, FastAPI

app = FastAPI()

def get_current_user():
    return {"username": "john_doe", "role": "admin"}

@app.get("/users/me")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return current_user
```

### Dependencies with Parameters
```python
def get_user_role(required_role: str):
    def dependency(current_user: dict = Depends(get_current_user)):
        if current_user["role"] != required_role:
            raise HTTPException(status_code=403, detail="Access denied")
        return current_user
    return dependency

@app.get("/admin")
async def admin_panel(user: dict = Depends(get_user_role("admin"))):
    return {"message": "Admin access granted"}
```

## Security Dependencies

### OAuth2 Password Bearer
```python
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # In real app, fetch user from database
    user = {"username": username}
    if user is None:
        raise credentials_exception
    return user
```

### API Key Authentication
```python
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def get_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)):
    api_key = credentials.credentials
    # Validate API key against database or config
    if api_key != "expected-api-key":
        raise HTTPException(status_code=403, detail="Invalid API key")
    return api_key

@app.get("/protected-endpoint")
async def protected_route(api_key: str = Depends(get_api_key)):
    return {"message": "Access granted with API key"}
```

## Database Dependencies

### Database Session Dependency
```python
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    # Use db session to query database
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

### Async Database Dependencies
```python
import asyncpg
from contextlib import asynccontextmanager

@asynccontextmanager
async def get_db_connection():
    conn = await asyncpg.connect("postgresql://user:pass@localhost/db")
    try:
        yield conn
    finally:
        await conn.close()

async def get_db():
    async with get_db_connection() as conn:
        yield conn

@app.get("/async-users/{user_id}")
async def get_async_user(user_id: int, db = Depends(get_db)):
    user = await db.fetchrow("SELECT * FROM users WHERE id = $1", user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return dict(user)
```

## Configuration Dependencies

### Environment-Based Configuration
```python
from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "FastAPI App"
    admin_email: str
    database_url: str
    debug: bool = False

    class Config:
        env_file = ".env"

def get_settings():
    return Settings()

@app.get("/info")
async def get_app_info(settings: Settings = Depends(get_settings)):
    return {
        "app_name": settings.app_name,
        "debug": settings.debug,
        "admin_email": settings.admin_email
    }
```

### Cached Dependencies
```python
from functools import lru_cache

@lru_cache()
def get_cached_settings():
    return Settings()

# This dependency will be cached and reused
@app.get("/cached-info")
async def get_cached_app_info(settings: Settings = Depends(get_cached_settings)):
    return settings
```

## Complex Dependencies

### Class-Based Dependencies
```python
class DatabaseService:
    def __init__(self, db_url: str):
        self.db_url = db_url
        self.connection = None

    async def connect(self):
        self.connection = await asyncpg.connect(self.db_url)

    async def disconnect(self):
        if self.connection:
            await self.connection.close()

    async def execute_query(self, query: str):
        if not self.connection:
            await self.connect()
        return await self.connection.fetch(query)

def get_database_service(db_url: str = Depends(lambda: DATABASE_URL)):
    return DatabaseService(db_url)

@app.on_event("startup")
async def startup_event():
    service = get_database_service()
    await service.connect()

@app.on_event("shutdown")
async def shutdown_event():
    service = get_database_service()
    await service.disconnect()
```

### Dependencies with Sub-Dependencies
```python
def get_user_from_token(token: str = Depends(oauth2_scheme)):
    # Validate token and return user
    pass

def get_admin_user(current_user: dict = Depends(get_user_from_token)):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

@app.get("/admin/users")
async def list_users(admin: dict = Depends(get_admin_user)):
    # Only accessible to admin users
    return {"users": []}
```

## Background Task Dependencies

### Background Task Registration
```python
from fastapi import BackgroundTasks

def send_notification_email(user_email: str, message: str):
    # Simulate sending email
    import time
    time.sleep(2)
    print(f"Email sent to {user_email}: {message}")

def register_background_task(background_tasks: BackgroundTasks):
    def add_task(email: str, msg: str):
        background_tasks.add_task(send_notification_email, email, msg)
    return add_task

@app.post("/send-notification")
async def send_notification(
    email: str,
    message: str,
    add_task = Depends(register_background_task)
):
    add_task(email, message)
    return {"message": "Notification queued"}
```

## Testing Dependencies

### Overriding Dependencies for Testing
```python
# In your test file
from fastapi.testclient import TestClient

def override_get_current_user():
    return {"username": "testuser", "role": "admin"}

# Override dependency for testing
app.dependency_overrides[get_current_user] = override_get_current_user

def test_protected_route():
    client = TestClient(app)
    response = client.get("/users/me")
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"
```

## Dependency Injection Best Practices

### 1. Use Clear Naming Conventions
- Prefix dependency functions with `get_`, `create_`, or `validate_`
- Use descriptive names that indicate the dependency's purpose

### 2. Handle Dependencies Gracefully
- Use try/finally blocks for resource cleanup
- Implement proper error handling in dependencies
- Consider caching for expensive operations

### 3. Organize Dependencies Logically
- Group related dependencies in modules
- Use dependency classes for complex scenarios
- Document dependencies clearly

### 4. Consider Performance Implications
- Cache expensive dependencies
- Use async dependencies when appropriate
- Minimize dependency chains

### 5. Test Dependencies Separately
- Mock dependencies in unit tests
- Use dependency overrides for integration tests
- Verify dependency behavior independently