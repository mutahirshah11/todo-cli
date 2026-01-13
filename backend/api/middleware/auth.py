from fastapi import HTTPException, status, Request
from fastapi.security.http import HTTPBearer, HTTPAuthorizationCredentials
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from typing import Optional
import logging
from ..utils.jwt_validator import verify_token, get_current_user_id
import time


class AuthMiddleware(BaseHTTPMiddleware):
    """
    Authentication middleware to verify JWT tokens for incoming requests.
    Applies authentication check to protected endpoints.
    """

    def __init__(self, app, exclude_paths: Optional[list] = None):
        """
        Initialize the authentication middleware.

        Args:
            app: FastAPI application instance
            exclude_paths: List of paths to exclude from authentication check
        """
        super().__init__(app)
        self.exclude_paths = exclude_paths or []
        self.security = HTTPBearer()
        self.logger = logging.getLogger(__name__)

    async def dispatch(self, request: Request, call_next):
        """
        Process the request and apply authentication check.

        Args:
            request: Incoming HTTP request
            call_next: Next middleware or endpoint handler

        Returns:
            HTTP response from the next handler
        """
        # Check if the path should be excluded from authentication
        if self._should_exclude_path(request.url.path):
            return await call_next(request)

        # Extract and validate the authorization header
        auth_header = request.headers.get("authorization")
        if not auth_header:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization header is missing"
            )

        # Validate the token
        try:
            # Extract token from header (remove "Bearer " prefix)
            if auth_header.startswith("Bearer "):
                token = auth_header[7:]  # Remove "Bearer " prefix
            else:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authorization header format"
                )

            # Verify the token
            payload = verify_token(token)

            # Add user info to request state for use in endpoints
            request.state.user_id = payload.get("sub")
            request.state.user_email = payload.get("email")

        except HTTPException:
            # Re-raise HTTP exceptions from token verification
            raise
        except Exception as e:
            # Handle any other errors during token verification
            self.logger.error(f"Authentication error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )

        # Continue with the request
        response = await call_next(request)
        return response

    def _should_exclude_path(self, path: str) -> bool:
        """
        Check if the given path should be excluded from authentication.

        Args:
            path: Request path to check

        Returns:
            True if path should be excluded, False otherwise
        """
        for exclude_path in self.exclude_paths:
            if path.startswith(exclude_path):
                return True
        return False


# Alternative approach using dependency injection for specific endpoints
async def require_authenticated_user(request: Request):
    """
    Dependency to require an authenticated user for specific endpoints.

    This can be used as a dependency in route handlers to ensure
    authentication is required for specific endpoints.

    Args:
        request: FastAPI request object

    Raises:
        HTTPException: If user is not authenticated
    """
    if not hasattr(request.state, 'user_id') or request.state.user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated"
        )
    return request.state.user_id


# Utility function to get current user ID from request state
def get_current_user_id_from_request(request: Request) -> str:
    """
    Get the current user ID from the request state.

    Args:
        request: FastAPI request object with user info in state

    Returns:
        User ID string
    """
    if not hasattr(request.state, 'user_id'):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated"
        )
    return request.state.user_id


# Example usage function for debugging
async def log_request_time(request: Request, call_next):
    """
    Middleware to log request processing time.
    This is for demonstration and can be combined with auth middleware.
    """
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    request.app.logger.info(f"Request {request.url} took {process_time:.2f}s")
    return response