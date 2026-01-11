"""
Comprehensive test suite for DELETE /api/{user_id}/tasks/{id} endpoint.
Tests all scenarios for deleting a task for a user.
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


def test_valid_deletion_of_existing_task():
    """T085 - Test valid deletion of existing task → 204 No Content."""
    token = create_test_token("user1")

    # First, create a task
    create_data = {"title": "Task to delete", "description": "This task will be deleted", "completed": False}
    response = client.post("/api/user1/tasks",
                          json=create_data,
                          headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    created_task = response.json()["task"]
    task_id = created_task["id"]
    assert task_id is not None

    # Now delete the task
    response = client.delete(f"/api/user1/tasks/{task_id}",
                            headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 204  # No Content

    # Verify the task is gone by trying to get it
    response_get = client.get(f"/api/user1/tasks/{task_id}",
                             headers={"Authorization": f"Bearer {token}"})
    assert response_get.status_code == 404  # Should not be found anymore


def test_deletion_of_non_existent_task():
    """T086 - Test deletion of non-existent task → 404 Not Found."""
    token = create_test_token("user1")

    response = client.delete("/api/user1/tasks/999999",  # Non-existent task ID
                            headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 404


def test_user_isolation_delete_task_owned_by_different_user():
    """T087 - Test user isolation (delete task owned by different user) → 403 Forbidden."""
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

    # Try to delete user1's task as user2 (should fail with 403)
    response = client.delete(f"/api/user1/tasks/{task_id}",
                            headers={"Authorization": f"Bearer {token_user2}"})
    assert response.status_code == 403  # Forbidden


def test_invalid_jwt_token():
    """T088 - Test invalid JWT token → 401 Unauthorized."""
    # Use an invalid/unsigned token
    invalid_token = "invalid.token.here"

    response = client.delete("/api/user1/tasks/1",
                            headers={"Authorization": f"Bearer {invalid_token}"})
    assert response.status_code == 401


def test_missing_jwt_token():
    """T089 - Test missing JWT token → 401 Unauthorized."""
    response = client.delete("/api/user1/tasks/1")  # No Authorization header
    assert response.status_code == 401


if __name__ == "__main__":
    # Run the tests
    test_valid_deletion_of_existing_task()
    test_deletion_of_non_existent_task()
    test_user_isolation_delete_task_owned_by_different_user()
    test_invalid_jwt_token()
    test_missing_jwt_token()
    print("All DELETE /api/{user_id}/tasks/{id} tests passed!")