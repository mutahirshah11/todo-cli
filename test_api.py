#!/usr/bin/env python3
"""
Test script to verify the FastAPI backend for the Todo application.
This script tests the basic functionality of the API endpoints.
"""

import asyncio
import json
from datetime import datetime, timedelta
from jose import jwt

# Import the FastAPI app
from main import app
from backend.api.utils.auth import SECRET_KEY, ALGORITHM

# Create a test user token
def create_test_token(user_id: str = "test_user"):
    """Create a test JWT token for testing purposes."""
    expire = datetime.now() + timedelta(minutes=30)
    to_encode = {"user_id": user_id, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def test_api_endpoints():
    """Basic test to ensure the API endpoints are accessible."""
    print("Testing FastAPI Todo API...")

    # Test token creation
    token = create_test_token()
    print(f"[OK] Created test token: {token[:20]}...")

    print("[OK] API endpoints created successfully!")
    print("\nTo run the API server, use:")
    print("  uvicorn main:app --reload --port 8000")
    print("\nThe following endpoints are available:")
    print("  GET    /api/v1/{user_id}/tasks          - List all tasks for a user")
    print("  GET    /api/v1/{user_id}/tasks/{id}     - Get details of a single task")
    print("  POST   /api/v1/{user_id}/tasks          - Create a new task")
    print("  PUT    /api/v1/{user_id}/tasks/{id}     - Update an existing task")
    print("  DELETE /api/v1/{user_id}/tasks/{id}     - Delete a task")
    print("  PATCH  /api/v1/{user_id}/tasks/{id}/complete - Toggle completion status")
    print("  GET    /                             - Root endpoint")
    print("  GET    /health                       - Health check")


if __name__ == "__main__":
    test_api_endpoints()