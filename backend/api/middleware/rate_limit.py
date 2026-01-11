"""
Rate limiting middleware for the Todo API.
Implements per-user rate limiting (1000 requests/hour/user).
"""
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import FastAPI, Request, Response
from ..utils.auth import verify_token
from typing import Dict
import time
import os


# Initialize rate limiter with default key function
limiter = Limiter(key_func=get_remote_address)


def get_user_rate_limit_key(request: Request) -> str:
    """
    Generate a rate limit key based on the authenticated user.
    This allows per-user rate limiting instead of per-IP.
    """
    try:
        # Extract user ID from Authorization header
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            payload = verify_token(token)
            if payload and "user_id" in payload:
                user_id = payload["user_id"]
                return f"user_{user_id}"
        # Fallback to IP address if no valid user found
        return get_remote_address(request)
    except:
        # Fallback to IP address if any error occurs
        return get_remote_address(request)


# Initialize the user-based limiter
user_limiter = Limiter(key_func=get_user_rate_limit_key)


def add_rate_limiting(app: FastAPI):
    """
    Add rate limiting to the FastAPI application.
    """
    app.state.limiter = user_limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


def rate_limit(limit: str = "1000/hour"):
    """
    Decorator to apply rate limiting to endpoints.
    Default is 1000 requests per hour per user.
    """
    return user_limiter.limit(limit)