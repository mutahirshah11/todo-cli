"""
Security tests for the Todo API.
Tests authentication, authorization, and other security measures.
"""
import pytest
from fastapi.testclient import TestClient
from main import app
from backend.api.utils.auth import SECRET_KEY, ALGORITHM
from jose import jwt
from datetime import datetime, timedelta


client = TestClient(app)


def create_test_token(user_id: str = "test_user"):
    """Create a test JWT token for testing purposes."""
    expire = datetime.now() + timedelta(minutes=30)
    to_encode = {"user_id": user_id, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def test_authentication_required():
    """Test that endpoints require authentication."""
    # Try to access an endpoint without authentication
    response = client.get("/api/user1/tasks")
    assert response.status_code == 401  # Unauthorized


def test_invalid_token():
    """Test handling of invalid tokens."""
    # Try to access with an invalid token
    response = client.get("/api/user1/tasks",
                         headers={"Authorization": "Bearer invalid_token"})
    assert response.status_code == 401  # Unauthorized


def test_user_isolation():
    """Test that users can't access other users' data."""
    token_user1 = create_test_token("user1")
    token_user2 = create_test_token("user2")

    # Create a task for user1
    create_data = {"title": "User1 task", "description": "Task for user1", "completed": False}
    response = client.post("/api/user1/tasks",
                          json=create_data,
                          headers={"Authorization": f"Bearer {token_user1}"})
    assert response.status_code == 201
    created_task = response.json()["task"]
    task_id = created_task["id"]

    # Try to access user1's task as user2
    response = client.get(f"/api/user1/tasks/{task_id}",
                         headers={"Authorization": f"Bearer {token_user2}"})
    assert response.status_code == 403  # Forbidden


def test_cross_user_modification_blocked():
    """Test that users can't modify other users' tasks."""
    token_user1 = create_test_token("user1")
    token_user2 = create_test_token("user2")

    # Create a task for user1
    create_data = {"title": "User1 task", "description": "Task for user1", "completed": False}
    response = client.post("/api/user1/tasks",
                          json=create_data,
                          headers={"Authorization": f"Bearer {token_user1}"})
    assert response.status_code == 201
    created_task = response.json()["task"]
    task_id = created_task["id"]

    # Try to update user1's task as user2
    update_data = {"title": "Hacked task", "description": "Hacked description", "completed": True}
    response = client.put(f"/api/user1/tasks/{task_id}",
                         json=update_data,
                         headers={"Authorization": f"Bearer {token_user2}"})
    assert response.status_code == 403  # Forbidden

    # Try to delete user1's task as user2
    response = client.delete(f"/api/user1/tasks/{task_id}",
                            headers={"Authorization": f"Bearer {token_user2}"})
    assert response.status_code == 403  # Forbidden


if __name__ == "__main__":
    test_authentication_required()
    test_invalid_token()
    test_user_isolation()
    test_cross_user_modification_blocked()
    print("All security tests passed!")