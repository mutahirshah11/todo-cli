"""
JWT validation utilities for backend services
This module provides token validation functionality that connects to the auth service
"""

from datetime import datetime, timedelta
import os
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from typing import Optional
import logging

# Secret key for JWT - should match the auth service
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

# Security scheme for FastAPI
security = HTTPBearer()

# Set up logging
logger = logging.getLogger(__name__)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a new access token with the provided data.

    Args:
        data: Dictionary containing the claims to include in the token
        expires_delta: Optional timedelta for token expiration (defaults to ACCESS_TOKEN_EXPIRE_MINUTES)

    Returns:
        Encoded JWT token string
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> dict:
    """
    Verify and decode a JWT token, returning the payload.

    Args:
        token: JWT token string to verify

    Returns:
        Decoded token payload as dictionary

    Raises:
        HTTPException: If token is invalid, expired, or cannot be decoded
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        logger.error(f"JWT verification error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user_id(token: str) -> str:
    """
    Extract user ID from a JWT token.

    Args:
        token: JWT token string

    Returns:
        User ID string from the 'sub' claim

    Raises:
        HTTPException: If token is invalid or user_id is not found
    """
    payload = verify_token(token)
    user_id: str = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_id


def verify_user_owns_resource(user_id: str, resource_owner_id: str) -> bool:
    """
    Verify that the authenticated user owns the resource.

    Args:
        user_id: The ID of the authenticated user
        resource_owner_id: The ID of the resource owner

    Returns:
        True if user owns the resource, raises HTTPException otherwise

    Raises:
        HTTPException: If user does not own the resource (403 Forbidden)
    """
    if user_id != resource_owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource"
        )
    return True


async def get_current_user_id_from_token_dep(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Dependency to get current user ID from JWT token.
    Verifies the token and returns the user ID.

    Args:
        credentials: HTTP authorization credentials from FastAPI security

    Returns:
        User ID string from the token
    """
    token = credentials.credentials
    try:
        user_id = get_current_user_id(token)
        return user_id
    except HTTPException:
        raise


def is_token_expired(token: str) -> bool:
    """
    Check if a JWT token is expired without raising an exception.

    Args:
        token: JWT token string to check

    Returns:
        True if token is expired, False otherwise
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_exp": True})
        return False
    except jwt.ExpiredSignatureError:
        return True
    except JWTError:
        # If there's any other error in decoding, treat as expired/invalid
        return True


def get_token_payload(token: str) -> Optional[dict]:
    """
    Get the payload from a JWT token without verifying expiration.

    Args:
        token: JWT token string

    Returns:
        Token payload as dictionary, or None if invalid
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_exp": False})
        return payload
    except JWTError:
        return None