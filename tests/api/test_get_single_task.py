"""
Comprehensive test suite for GET /api/tasks/{id} endpoint.
Tests all scenarios for getting a single task for the authenticated user.
"""
import pytest
from fastapi.testclient import TestClient
from backend.main import app
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
    response = client.post("/api/tasks",
                          json=task_data,
                          headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    created_task = response.json()["task"]
    task_id = created_task["id"]

    # Now get the specific task
    response = client.get(f"/api/tasks/{task_id}",
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
    response = client.get("/api/tasks/999999",
                         headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 404


def test_user_isolation_cross_user_access():
    """T040 - Test user isolation (cross-user access) - each user can only access their own tasks."""
    # Create tokens for two different users
    token_user1 = create_test_token("user1")
    token_user2 = create_test_token("user2")

    # Create a task for user1
    task_data = {"title": "User1 task", "description": "Task for user1", "completed": False}
    response = client.post("/api/tasks",
                          json=task_data,
                          headers={"Authorization": f"Bearer {token_user1}"})
    assert response.status_code == 201
    created_task = response.json()["task"]
    task_id = created_task["id"]
    assert task_id is not None

    # Try to access user1's task as user2 (should return 404 since user2 doesn't have that task)
    response = client.get(f"/api/tasks/{task_id}",
                         headers={"Authorization": f"Bearer {token_user2}"})
    # With the new implementation, users can't access each other's tasks,
    # so this will likely return 404 (not found) instead of 403 (forbidden)
    assert response.status_code in [403, 404]  # Could be either depending on implementation


def test_invalid_jwt_token():
    """T041 - Test invalid JWT token → 401 Unauthorized."""
    # Use an invalid/unsigned token
    invalid_token = "invalid.token.here"

    response = client.get("/api/tasks/1",
                         headers={"Authorization": f"Bearer {invalid_token}"})
    assert response.status_code == 401


def test_missing_jwt_token():
    """T042 - Test missing JWT token → 401 Unauthorized."""
    response = client.get("/api/tasks/1")  # No Authorization header
    assert response.status_code == 401


# Remove the user_id_mismatch test since the user_id is no longer in the path
# The user_id is now extracted from the token, so there's no possibility of mismatch


if __name__ == "__main__":
    # Run the tests
    test_valid_request_for_existing_task()
    test_request_for_non_existent_task()
    test_user_isolation_cross_user_access()
    test_invalid_jwt_token()
    test_missing_jwt_token()
    print("All GET /api/tasks/{id} tests passed!")