# Testing FastAPI Applications

## Unit Testing Dependencies

### Testing Individual Functions
```python
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

def test_create_access_token():
    data = {"sub": "testuser"}
    token = create_access_token(data, expires_delta=timedelta(minutes=15))

    # Verify token is created
    assert isinstance(token, str)
    assert len(token) > 0

    # Verify token can be decoded
    decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded["sub"] == "testuser"
```

### Testing Pydantic Models
```python
def test_item_create_model():
    # Valid data
    item = ItemCreate(
        name="Test Item",
        description="A test item",
        price=10.99,
        category="electronics"
    )
    assert item.name == "Test Item"
    assert item.price == 10.99

def test_item_create_invalid_data():
    # Invalid data should raise validation error
    with pytest.raises(ValidationError):
        ItemCreate(name="", price=-5, category="electronics")
```

## Integration Testing with TestClient

### Basic Route Testing
```python
from fastapi.testclient import TestClient

# Import your main app
from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

def test_create_item():
    item_data = {
        "name": "Test Item",
        "description": "A test item",
        "price": 10.99,
        "category": "electronics"
    }

    response = client.post("/items/", json=item_data)
    assert response.status_code == 200

    response_data = response.json()
    assert response_data["name"] == item_data["name"]
    assert response_data["price"] == item_data["price"]
```

### Testing with Authentication
```python
def test_protected_route():
    # Mock token for testing
    token = create_access_token(data={"sub": "testuser"})

    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_unauthorized_access():
    response = client.get("/users/me")
    assert response.status_code == 401
```

## Dependency Override Testing

### Mocking Database Dependencies
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Override the dependency
app.dependency_overrides[get_db] = override_get_db

def test_read_items():
    response = client.get("/items/")
    assert response.status_code == 200
```

### Mocking External Services
```python
def test_background_task():
    with patch('main.send_email_task') as mock_send_email:
        response = client.post("/send-email/", params={
            "email": "test@example.com",
            "message": "Test message"
        })

        assert response.status_code == 200
        # Verify background task was registered
        assert "queued" in response.json()["message"]
        # Note: Background tasks run after response, so mock assertion happens after
```

## Testing Different HTTP Methods

### CRUD Operation Tests
```python
def test_crud_operations():
    # Create
    item_data = {"name": "Test Item", "price": 10.99, "category": "electronics"}
    create_response = client.post("/items/", json=item_data)
    assert create_response.status_code == 200

    created_item = create_response.json()
    item_id = created_item["id"]

    # Read
    read_response = client.get(f"/items/{item_id}")
    assert read_response.status_code == 200
    assert read_response.json()["name"] == "Test Item"

    # Update
    update_data = {"name": "Updated Item", "price": 15.99, "category": "electronics"}
    update_response = client.put(f"/items/{item_id}", json=update_data)
    assert update_response.status_code == 200
    assert update_response.json()["name"] == "Updated Item"

    # Delete
    delete_response = client.delete(f"/items/{item_id}")
    assert delete_response.status_code == 200
```

### Testing Query Parameters
```python
def test_query_parameters():
    response = client.get("/items/?skip=0&limit=10&q=test")
    assert response.status_code == 200

    # Test validation
    response = client.get("/items/?skip=-1&limit=10")  # skip should be >= 0
    assert response.status_code == 422

def test_path_parameters():
    response = client.get("/items/123")
    assert response.status_code == 200

    # Test validation
    response = client.get("/items/abc")  # should be integer
    assert response.status_code == 422
```

## Testing File Uploads

### Single File Upload Test
```python
def test_file_upload():
    # Create a test file
    test_file_content = b"test file content"
    test_file = io.BytesIO(test_file_content)

    response = client.post(
        "/upload/",
        files={"file": ("test.txt", test_file, "text/plain")}
    )

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["filename"] == "test.txt"
    assert response_data["content_type"] == "text/plain"

def test_file_validation():
    large_file = io.BytesIO(b"x" * (6 * 1024 * 1024))  # 6MB file

    response = client.post(
        "/upload/",
        files={"file": ("large.txt", large_file, "text/plain")}
    )

    # Should fail validation (too large)
    assert response.status_code == 413
```

## Testing Error Handling

### HTTPException Tests
```python
def test_http_exception():
    response = client.get("/items/999")  # Assuming this item doesn't exist
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

def test_validation_error():
    invalid_item = {
        "name": "",  # Empty name not allowed
        "price": -5,  # Negative price not allowed
        "category": "electronics"
    }

    response = client.post("/items/", json=invalid_item)
    assert response.status_code == 422  # Validation error
```

### Custom Exception Handler Tests
```python
def test_custom_exception_handler():
    # Test with invalid request that triggers custom handler
    response = client.post("/invalid-endpoint", json={"invalid": "data"})
    # Verify custom error format is returned
    assert "error" in response.json() or response.status_code in [400, 422]
```

## WebSocket Testing

### WebSocket Connection Test
```python
import websockets
import asyncio

@pytest.mark.asyncio
async def test_websocket():
    async with websockets.connect("ws://localhost:8000/ws") as websocket:
        # Send message
        await websocket.send("Hello")

        # Receive response
        response = await websocket.recv()
        assert "Hello" in response
```

## Testing Best Practices

### 1. Use Fixtures for Common Setup
```python
@pytest.fixture(scope="module")
def test_client():
    client = TestClient(app)
    yield client

@pytest.fixture
def mock_db_session():
    session = MagicMock()
    yield session
```

### 2. Test Both Happy and Sad Paths
- Test successful operations
- Test error conditions
- Test validation failures
- Test edge cases

### 3. Isolate Tests
- Use separate test database
- Clean up test data after each test
- Use dependency overrides to isolate from external services

### 4. Test Security
- Test unauthorized access
- Test invalid tokens
- Test rate limiting (if implemented)
- Test input sanitization

### 5. Performance Testing
```python
import time

def test_endpoint_performance():
    start_time = time.time()
    response = client.get("/items/")
    end_time = time.time()

    # Assert response time is acceptable
    assert (end_time - start_time) < 1.0  # Less than 1 second
```

### 6. Test API Documentation
```python
def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200

    schema = response.json()
    assert "paths" in schema
    assert "/items/" in schema["paths"]
```

## Running Tests

### Basic Test Command
```bash
pytest
```

### With Coverage
```bash
pytest --cov=main --cov-report=html
```

### With Specific Tags
```bash
pytest -m "integration"  # Run only integration tests
pytest -m "unit"         # Run only unit tests
```

### Continuous Integration Setup
```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.10
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov
    - name: Run tests
      run: pytest --cov=main --cov-report=xml
```