"""
Minimal JWT validation utilities for backend services
This module provides token validation functionality that connects to the auth service
"""

from datetime import datetime
import os
from fastapi import HTTPException, status
from jose import JWTError, jwt
from typing import Optional

# Secret key for JWT - should match the auth service
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"


def verify_token(token: str):
    """Verify and decode a JWT token, returning the payload."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user_id(token: str) -> str:
    """Extract user ID from a JWT token."""
    payload = verify_token(token)
    user_id: str = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_id


def verify_user_owns_resource(user_id: str, resource_owner_id: str):
    """
    Verify that the authenticated user owns the resource.
    Raises 403 Forbidden if the user doesn't own the resource.
    """
    if user_id != resource_owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource"
        )