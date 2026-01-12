from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Todo API"}

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_get_tasks_without_auth():
    # This should return 401 or 403 depending on the implementation
    response = client.get("/api/v1/123/tasks")
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.text}")
    # Since there's no auth header, it should return 401/403
    # HTTPBearer may return 403 if no credentials provided
    assert response.status_code in [401, 403], f"Expected 401 or 403, got {response.status_code}"

if __name__ == "__main__":
    test_root_endpoint()
    test_health_endpoint()
    test_get_tasks_without_auth()
    print("All tests passed!")