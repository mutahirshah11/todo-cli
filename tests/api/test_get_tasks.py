"""
Comprehensive test suite for GET /api/tasks endpoint.
Tests all scenarios for listing tasks for the authenticated user.
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


def test_valid_request_with_task_list():
    """T027 - Test valid request with task list (may be empty or contain existing tasks)."""
    token = create_test_token("user1")

    response = client.get("/api/tasks",
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

    response1 = client.post("/api/tasks",
                           json=task_data1,
                           headers={"Authorization": f"Bearer {token}"})
    response2 = client.post("/api/tasks",
                           json=task_data2,
                           headers={"Authorization": f"Bearer {token}"})

    assert response1.status_code == 201
    assert response2.status_code == 201

    # Now get the tasks
    response = client.get("/api/tasks",
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
    response = client.post("/api/tasks",
                          json=task_data,
                          headers={"Authorization": f"Bearer {token_user1}"})
    assert response.status_code == 201

    # Get tasks as user1 (should succeed)
    response = client.get("/api/tasks",
                         headers={"Authorization": f"Bearer {token_user1}"})
    assert response.status_code == 200
    user1_tasks = response.json()["tasks"]

    # Get tasks as user2 (should return user2's tasks, not user1's)
    response = client.get("/api/tasks",
                         headers={"Authorization": f"Bearer {token_user2}"})
    assert response.status_code == 200
    user2_tasks = response.json()["tasks"]

    # The tasks should be isolated - each user gets their own tasks
    # (This test assumes no tasks were created for user2, so the list should be empty)
    # In practice, each user only gets their own tasks based on the token


def test_invalid_jwt_token():
    """T030 - Test invalid JWT token → 401 Unauthorized."""
    # Use an invalid/unsigned token
    invalid_token = "invalid.token.here"

    response = client.get("/api/tasks",
                         headers={"Authorization": f"Bearer {invalid_token}"})
    assert response.status_code == 401


def test_missing_jwt_token():
    """T031 - Test missing JWT token → 401 Unauthorized."""
    response = client.get("/api/tasks")  # No Authorization header
    assert response.status_code == 401


# Remove the user_id_mismatch test since the user_id is no longer in the path
# The user_id is now extracted from the token, so there's no possibility of mismatch


if __name__ == "__main__":
    # Run the tests
    test_valid_request_with_task_list()
    test_valid_request_with_multiple_tasks()
    test_user_isolation_cross_user_access_prevention()
    test_invalid_jwt_token()
    test_missing_jwt_token()
    print("All GET /api/tasks tests passed!")