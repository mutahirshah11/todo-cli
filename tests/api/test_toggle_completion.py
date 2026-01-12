"""
Comprehensive test suite for PATCH /api/{user_id}/tasks/{id}/complete endpoint.
Tests all scenarios for toggling completion status of a task for a user.
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


def test_valid_toggle_of_completion_status_false_to_true():
    """T074 - Test valid toggle of completion status (false to true)."""
    token = create_test_token("user1")

    # First, create a task (by default it will be not completed)
    create_data = {"title": "Incomplete task", "description": "Task to be completed", "completed": False}
    response = client.post("/api/user1/tasks",
                          json=create_data,
                          headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    created_task = response.json()["task"]
    task_id = created_task["id"]
    assert task_id is not None
    assert created_task["completed"] == False

    # Now toggle the completion status to true
    toggle_data = {"completed": True}
    response = client.patch(f"/api/user1/tasks/{task_id}/complete",
                           json=toggle_data,
                           headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    data = response.json()
    assert "task" in data
    task = data["task"]
    assert task["id"] == task_id
    assert task["completed"] == True


def test_valid_toggle_of_completion_status_true_to_false():
    """T075 - Test valid toggle of completion status (true to false)."""
    token = create_test_token("user1")

    # First, create a completed task
    create_data = {"title": "Complete task", "description": "Task that is already completed", "completed": True}
    response = client.post("/api/user1/tasks",
                          json=create_data,
                          headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    created_task = response.json()["task"]
    task_id = created_task["id"]
    assert task_id is not None
    assert created_task["completed"] == True

    # Now toggle the completion status to false
    toggle_data = {"completed": False}
    response = client.patch(f"/api/user1/tasks/{task_id}/complete",
                           json=toggle_data,
                           headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    data = response.json()
    assert "task" in data
    task = data["task"]
    assert task["id"] == task_id
    assert task["completed"] == False


def test_toggle_of_non_existent_task():
    """T076 - Test toggle of non-existent task → 404 Not Found."""
    token = create_test_token("user1")

    toggle_data = {"completed": True}
    response = client.patch("/api/user1/tasks/999999/complete",  # Non-existent task ID
                           json=toggle_data,
                           headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 404


def test_user_isolation_toggle_task_owned_by_different_user():
    """T077 - Test user isolation (toggle task owned by different user) → 403 Forbidden."""
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

    # Try to toggle user1's task as user2 (should fail with 403)
    toggle_data = {"completed": True}
    response = client.patch(f"/api/user1/tasks/{task_id}/complete",
                           json=toggle_data,
                           headers={"Authorization": f"Bearer {token_user2}"})
    assert response.status_code == 403  # Forbidden


def test_invalid_jwt_token():
    """T078 - Test invalid JWT token → 401 Unauthorized."""
    # Use an invalid/unsigned token
    invalid_token = "invalid.token.here"

    toggle_data = {"completed": True}
    response = client.patch("/api/user1/tasks/1/complete",
                           json=toggle_data,
                           headers={"Authorization": f"Bearer {invalid_token}"})
    assert response.status_code == 401


def test_missing_jwt_token():
    """T079 - Test missing JWT token → 401 Unauthorized."""
    toggle_data = {"completed": True}
    response = client.patch("/api/user1/tasks/1/complete",
                           json=toggle_data)  # No Authorization header
    assert response.status_code == 401


def test_invalid_request_body():
    """T080 - Test invalid request body → 422 Unprocessable Entity."""
    token = create_test_token("user1")

    # First, create a task
    create_data = {"title": "Test task", "description": "Test description", "completed": False}
    response = client.post("/api/user1/tasks",
                          json=create_data,
                          headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    created_task = response.json()["task"]
    task_id = created_task["id"]
    assert task_id is not None

    # Try to toggle with invalid request body (no completed field)
    invalid_data = {}  # Missing required 'completed' field
    response = client.patch(f"/api/user1/tasks/{task_id}/complete",
                           json=invalid_data,
                           headers={"Authorization": f"Bearer {token}"})

    assert response.status_code in [400, 422]  # FastAPI returns 422 for validation errors


if __name__ == "__main__":
    # Run the tests
    test_valid_toggle_of_completion_status_false_to_true()
    test_valid_toggle_of_completion_status_true_to_false()
    test_toggle_of_non_existent_task()
    test_user_isolation_toggle_task_owned_by_different_user()
    test_invalid_jwt_token()
    test_missing_jwt_token()
    test_invalid_request_body()
    print("All PATCH /api/{user_id}/tasks/{id}/complete tests passed!")