"""
Comprehensive test suite for GET /api/{user_id}/tasks/{id} endpoint.
Tests all scenarios for getting a single task for a user.
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


def test_valid_request_for_existing_task():
    """T038 - Test valid request for existing task."""
    token = create_test_token("user1")

    # First, create a task
    task_data = {"title": "Test task", "description": "Test description", "completed": False}
    response = client.post("/api/user1/tasks",
                          json=task_data,
                          headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    created_task = response.json()["task"]
    task_id = created_task["id"]

    # Now get the specific task
    response = client.get(f"/api/user1/tasks/{task_id}",
                         headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    data = response.json()
    assert "task" in data
    task = data["task"]
    assert task["id"] == task_id
    assert task["title"] == "Test task"
    assert task["description"] == "Test description"
    assert task["completed"] == False
    assert task["user_id"] == "user1"


def test_request_for_non_existent_task():
    """T039 - Test request for non-existent task → 404 Not Found."""
    token = create_test_token("user1")

    # Try to get a task with a non-existent ID
    response = client.get("/api/user1/tasks/999999",
                         headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 404


def test_user_isolation_cross_user_access():
    """T040 - Test user isolation (cross-user access) → 403 Forbidden."""
    # Create tokens for two different users
    token_user1 = create_test_token("user1")
    token_user2 = create_test_token("user2")

    # Create a task for user1
    task_data = {"title": "User1 task", "description": "Task for user1", "completed": False}
    response = client.post("/api/user1/tasks",
                          json=task_data,
                          headers={"Authorization": f"Bearer {token_user1}"})
    assert response.status_code == 201
    created_task = response.json()["task"]
    task_id = created_task["id"]
    assert task_id is not None

    # Try to access user1's task as user2 (should fail with 403)
    response = client.get(f"/api/user1/tasks/{task_id}",
                         headers={"Authorization": f"Bearer {token_user2}"})
    assert response.status_code == 403  # Forbidden


def test_invalid_jwt_token():
    """T041 - Test invalid JWT token → 401 Unauthorized."""
    # Use an invalid/unsigned token
    invalid_token = "invalid.token.here"

    response = client.get("/api/user1/tasks/1",
                         headers={"Authorization": f"Bearer {invalid_token}"})
    assert response.status_code == 401


def test_missing_jwt_token():
    """T042 - Test missing JWT token → 401 Unauthorized."""
    response = client.get("/api/user1/tasks/1")  # No Authorization header
    assert response.status_code == 401


def test_user_id_mismatch_in_path_vs_token():
    """T043 - Test user ID mismatch in path vs token → 403 Forbidden."""
    # Token for user1, but trying to access user2's task
    token_for_user1 = create_test_token("user1")

    response = client.get("/api/user2/tasks/1",  # Path says user2
                         headers={"Authorization": f"Bearer {token_for_user1}"})  # Token says user1
    assert response.status_code == 403  # Forbidden due to mismatch


if __name__ == "__main__":
    # Run the tests
    test_valid_request_for_existing_task()
    test_request_for_non_existent_task()
    test_user_isolation_cross_user_access()
    test_invalid_jwt_token()
    test_missing_jwt_token()
    test_user_id_mismatch_in_path_vs_token()
    print("All GET /api/{user_id}/tasks/{id} tests passed!")