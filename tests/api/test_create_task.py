"""
Comprehensive test suite for POST /api/tasks endpoint.
Tests all scenarios for creating a new task for the authenticated user.
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


def test_valid_creation_with_minimal_data():
    """T049 - Test valid creation with minimal data (title only)."""
    token = create_test_token("user1")

    task_data = {"title": "Minimal task"}
    response = client.post("/api/tasks",
                          json=task_data,
                          headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 201
    data = response.json()
    assert "task" in data
    task = data["task"]
    assert task["title"] == "Minimal task"
    assert task["description"] == ""  # Default empty description
    assert task["completed"] == False  # Default to False
    assert task["user_id"] == "user1"


def test_valid_creation_with_all_fields():
    """T050 - Test valid creation with all fields (title, description, completed)."""
    token = create_test_token("user1")

    task_data = {
        "title": "Complete task",
        "description": "A task with all fields filled",
        "completed": True
    }
    response = client.post("/api/tasks",
                          json=task_data,
                          headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 201
    data = response.json()
    assert "task" in data
    task = data["task"]
    assert task["title"] == "Complete task"
    assert task["description"] == "A task with all fields filled"
    assert task["completed"] == True
    assert task["user_id"] == "user1"


def test_creation_with_invalid_title_empty():
    """T051 - Test creation with invalid title (empty) → 422 Unprocessable Entity."""
    token = create_test_token("user1")

    task_data = {"title": "", "description": "A task with empty title", "completed": False}
    response = client.post("/api/tasks",
                          json=task_data,
                          headers={"Authorization": f"Bearer {token}"})

    assert response.status_code in [400, 422]  # FastAPI returns 422 for validation errors


def test_creation_with_invalid_title_over_100_chars():
    """T052 - Test creation with invalid title (over 100 chars) → 422 Unprocessable Entity."""
    token = create_test_token("user1")

    long_title = "A" * 101  # 101 characters, exceeding the limit
    task_data = {"title": long_title, "description": "A task with long title", "completed": False}
    response = client.post("/api/tasks",
                          json=task_data,
                          headers={"Authorization": f"Bearer {token}"})

    assert response.status_code in [400, 422]  # FastAPI returns 422 for validation errors


def test_creation_with_invalid_description_over_500_chars():
    """T053 - Test creation with invalid description (over 500 chars) → 422 Unprocessable Entity."""
    token = create_test_token("user1")

    long_description = "A" * 501  # 501 characters, exceeding the limit
    task_data = {"title": "Valid title", "description": long_description, "completed": False}
    response = client.post("/api/tasks",
                          json=task_data,
                          headers={"Authorization": f"Bearer {token}"})

    assert response.status_code in [400, 422]  # FastAPI returns 422 for validation errors


def test_invalid_jwt_token():
    """T054 - Test invalid JWT token → 401 Unauthorized."""
    # Use an invalid/unsigned token
    invalid_token = "invalid.token.here"

    task_data = {"title": "Test task", "description": "Test description", "completed": False}
    response = client.post("/api/tasks",
                          json=task_data,
                          headers={"Authorization": f"Bearer {invalid_token}"})
    assert response.status_code == 401


def test_missing_jwt_token():
    """T055 - Test missing JWT token → 401 Unauthorized."""
    task_data = {"title": "Test task", "description": "Test description", "completed": False}
    response = client.post("/api/tasks",
                          json=task_data)  # No Authorization header
    assert response.status_code == 401


if __name__ == "__main__":
    # Run the tests
    test_valid_creation_with_minimal_data()
    test_valid_creation_with_all_fields()
    test_creation_with_invalid_title_empty()
    test_creation_with_invalid_title_over_100_chars()
    test_creation_with_invalid_description_over_500_chars()
    test_invalid_jwt_token()
    test_missing_jwt_token()
    print("All POST /api/tasks tests passed!")