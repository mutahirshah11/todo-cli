"""
Comprehensive test suite for PUT /api/{user_id}/tasks/{id} endpoint.
Tests all scenarios for updating an existing task for a user.
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


def test_valid_update_of_existing_task():
    """T061 - Test valid update of existing task."""
    token = create_test_token("user1")

    # First, create a task
    create_data = {"title": "Original task", "description": "Original description", "completed": False}
    response = client.post("/api/user1/tasks",
                          json=create_data,
                          headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    created_task = response.json()["task"]
    task_id = created_task["id"]
    assert task_id is not None

    # Now update the task
    update_data = {
        "title": "Updated task",
        "description": "Updated description",
        "completed": True
    }
    response = client.put(f"/api/user1/tasks/{task_id}",
                         json=update_data,
                         headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    data = response.json()
    assert "task" in data
    task = data["task"]
    assert task["id"] == task_id
    assert task["title"] == "Updated task"
    assert task["description"] == "Updated description"
    assert task["completed"] == True


def test_update_of_non_existent_task():
    """T062 - Test update of non-existent task → 404 Not Found."""
    token = create_test_token("user1")

    update_data = {
        "title": "Updated task",
        "description": "Updated description",
        "completed": True
    }
    response = client.put("/api/user1/tasks/999999",  # Non-existent task ID
                         json=update_data,
                         headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 404


def test_update_with_invalid_title_empty():
    """T063 - Test update with invalid title (empty) → 422 Unprocessable Entity."""
    token = create_test_token("user1")

    # First, create a task
    create_data = {"title": "Original task", "description": "Original description", "completed": False}
    response = client.post("/api/user1/tasks",
                          json=create_data,
                          headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    created_task = response.json()["task"]
    task_id = created_task["id"]
    assert task_id is not None

    # Now try to update with empty title
    update_data = {
        "title": "",  # Empty title should fail validation
        "description": "Updated description",
        "completed": True
    }
    response = client.put(f"/api/user1/tasks/{task_id}",
                         json=update_data,
                         headers={"Authorization": f"Bearer {token}"})

    assert response.status_code in [400, 422]  # FastAPI returns 422 for validation errors


def test_update_with_invalid_title_over_100_chars():
    """T064 - Test update with invalid title (over 100 chars) → 422 Unprocessable Entity."""
    token = create_test_token("user1")

    # First, create a task
    create_data = {"title": "Original task", "description": "Original description", "completed": False}
    response = client.post("/api/user1/tasks",
                          json=create_data,
                          headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    created_task = response.json()["task"]
    task_id = created_task["id"]
    assert task_id is not None

    # Now try to update with a very long title
    long_title = "A" * 101  # 101 characters, exceeding the limit
    update_data = {
        "title": long_title,
        "description": "Updated description",
        "completed": True
    }
    response = client.put(f"/api/user1/tasks/{task_id}",
                         json=update_data,
                         headers={"Authorization": f"Bearer {token}"})

    assert response.status_code in [400, 422]  # FastAPI returns 422 for validation errors


def test_update_with_invalid_description_over_500_chars():
    """T065 - Test update with invalid description (over 500 chars) → 422 Unprocessable Entity."""
    token = create_test_token("user1")

    # First, create a task
    create_data = {"title": "Original task", "description": "Original description", "completed": False}
    response = client.post("/api/user1/tasks",
                          json=create_data,
                          headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    created_task = response.json()["task"]
    task_id = created_task["id"]
    assert task_id is not None

    # Now try to update with a very long description
    long_description = "A" * 501  # 501 characters, exceeding the limit
    update_data = {
        "title": "Updated title",
        "description": long_description,
        "completed": True
    }
    response = client.put(f"/api/user1/tasks/{task_id}",
                         json=update_data,
                         headers={"Authorization": f"Bearer {token}"})

    assert response.status_code in [400, 422]  # FastAPI returns 422 for validation errors


def test_user_isolation_update_task_owned_by_different_user():
    """T066 - Test user isolation (update task owned by different user) → 403 Forbidden."""
    # Create tokens for two different users
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
    assert task_id is not None

    # Try to update user1's task as user2 (should fail with 403)
    update_data = {
        "title": "Hacked task",
        "description": "Hacked description",
        "completed": True
    }
    response = client.put(f"/api/user1/tasks/{task_id}",
                         json=update_data,
                         headers={"Authorization": f"Bearer {token_user2}"})
    assert response.status_code == 403  # Forbidden


def test_invalid_jwt_token():
    """T067 - Test invalid JWT token → 401 Unauthorized."""
    # Use an invalid/unsigned token
    invalid_token = "invalid.token.here"

    update_data = {
        "title": "Updated task",
        "description": "Updated description",
        "completed": True
    }
    response = client.put("/api/user1/tasks/1",
                         json=update_data,
                         headers={"Authorization": f"Bearer {invalid_token}"})
    assert response.status_code == 401


def test_missing_jwt_token():
    """T068 - Test missing JWT token → 401 Unauthorized."""
    update_data = {
        "title": "Updated task",
        "description": "Updated description",
        "completed": True
    }
    response = client.put("/api/user1/tasks/1",
                         json=update_data)  # No Authorization header
    assert response.status_code == 401


if __name__ == "__main__":
    # Run the tests
    test_valid_update_of_existing_task()
    test_update_of_non_existent_task()
    test_update_with_invalid_title_empty()
    test_update_with_invalid_title_over_100_chars()
    test_update_with_invalid_description_over_500_chars()
    test_user_isolation_update_task_owned_by_different_user()
    test_invalid_jwt_token()
    test_missing_jwt_token()
    print("All PUT /api/{user_id}/tasks/{id} tests passed!")