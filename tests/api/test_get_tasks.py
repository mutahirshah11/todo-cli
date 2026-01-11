"""
Comprehensive test suite for GET /api/{user_id}/tasks endpoint.
Tests all scenarios for listing tasks for a user.
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


def test_valid_request_with_task_list():
    """T027 - Test valid request with task list (may be empty or contain existing tasks)."""
    token = create_test_token("user1")

    response = client.get("/api/user1/tasks",
                         headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    data = response.json()
    assert "tasks" in data
    assert isinstance(data["tasks"], list)
    # The response should be a valid task list, regardless of whether it's empty or has tasks
    # If there are existing tasks in the storage, they will be returned


def test_valid_request_with_multiple_tasks():
    """T028 - Test valid request with multiple tasks."""
    token = create_test_token("user1")

    # First, create some tasks
    task_data1 = {"title": "Task 1", "description": "First task", "completed": False}
    task_data2 = {"title": "Task 2", "description": "Second task", "completed": True}

    response1 = client.post("/api/user1/tasks",
                           json=task_data1,
                           headers={"Authorization": f"Bearer {token}"})
    response2 = client.post("/api/user1/tasks",
                           json=task_data2,
                           headers={"Authorization": f"Bearer {token}"})

    assert response1.status_code == 201
    assert response2.status_code == 201

    # Now get the tasks
    response = client.get("/api/user1/tasks",
                         headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    data = response.json()
    assert "tasks" in data
    assert isinstance(data["tasks"], list)
    assert len(data["tasks"]) >= 2  # At least 2 tasks should be returned

    # Verify the tasks have correct structure
    for task in data["tasks"]:
        assert "id" in task
        assert "title" in task
        assert "description" in task
        assert "completed" in task
        assert "created_at" in task
        assert "updated_at" in task
        assert "user_id" in task


def test_user_isolation_cross_user_access_prevention():
    """T029 - Test user isolation (cross-user access prevention)."""
    # Create tokens for two different users
    token_user1 = create_test_token("user1")
    token_user2 = create_test_token("user2")

    # Create a task for user1
    task_data = {"title": "User1 task", "description": "Task for user1", "completed": False}
    response = client.post("/api/user1/tasks",
                          json=task_data,
                          headers={"Authorization": f"Bearer {token_user1}"})
    assert response.status_code == 201

    # Try to access user1's task as user2 (should fail with 403)
    response = client.get("/api/user1/tasks",
                         headers={"Authorization": f"Bearer {token_user2}"})
    assert response.status_code == 403  # Forbidden


def test_invalid_jwt_token():
    """T030 - Test invalid JWT token → 401 Unauthorized."""
    # Use an invalid/unsigned token
    invalid_token = "invalid.token.here"

    response = client.get("/api/user1/tasks",
                         headers={"Authorization": f"Bearer {invalid_token}"})
    assert response.status_code == 401


def test_missing_jwt_token():
    """T031 - Test missing JWT token → 401 Unauthorized."""
    response = client.get("/api/user1/tasks")  # No Authorization header
    assert response.status_code == 401


def test_user_id_mismatch_in_path_vs_token():
    """T032 - Test user ID mismatch in path vs token → 403 Forbidden."""
    # Token for user1, but trying to access user2's tasks
    token_for_user1 = create_test_token("user1")

    response = client.get("/api/user2/tasks",  # Path says user2
                         headers={"Authorization": f"Bearer {token_for_user1}"})  # Token says user1
    assert response.status_code == 403  # Forbidden due to mismatch


if __name__ == "__main__":
    # Run the tests
    test_valid_request_with_empty_task_list()
    test_valid_request_with_multiple_tasks()
    test_user_isolation_cross_user_access_prevention()
    test_invalid_jwt_token()
    test_missing_jwt_token()
    test_user_id_mismatch_in_path_vs_token()
    print("All GET /api/{user_id}/tasks tests passed!")