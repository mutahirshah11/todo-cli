from fastapi.testclient import TestClient
from main import app
from backend.api.utils.auth import SECRET_KEY, ALGORITHM
from jose import jwt
from datetime import datetime, timedelta
import json

client = TestClient(app)

def create_test_token(user_id: str = "test_user"):
    """Create a test JWT token for testing purposes."""
    expire = datetime.now() + timedelta(minutes=30)
    to_encode = {"user_id": user_id, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Todo API"}

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_get_tasks_without_auth():
    # This should return 401 since no auth header is provided
    response = client.get("/api/v1/123/tasks")
    assert response.status_code == 401

def test_get_tasks_with_auth():
    # Create a token with user_id that matches the path
    token = create_test_token("test_user")

    # This should work if user_id in token matches path
    response = client.get("/api/v1/test_user/tasks",
                         headers={"Authorization": f"Bearer {token}"})
    # Should return 200 with empty task list
    assert response.status_code == 200
    data = response.json()
    assert "tasks" in data
    assert isinstance(data["tasks"], list)

def test_get_tasks_user_mismatch():
    # Create a token with different user_id than in path
    token = create_test_token("user1")

    # This should return 403 since user_id in token doesn't match path
    response = client.get("/api/v1/user2/tasks",
                         headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403

def test_create_task():
    token = create_test_token("test_user")

    # Test creating a task
    task_data = {
        "title": "Test task",
        "description": "Test description",
        "completed": False
    }

    response = client.post("/api/v1/test_user/tasks",
                          json=task_data,
                          headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201

    data = response.json()
    assert "task" in data
    assert data["task"]["title"] == "Test task"
    assert data["task"]["description"] == "Test description"

if __name__ == "__main__":
    test_root_endpoint()
    test_health_endpoint()
    test_get_tasks_without_auth()
    test_get_tasks_with_auth()
    test_get_tasks_user_mismatch()
    test_create_task()
    print("All API tests passed!")