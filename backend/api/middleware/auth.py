from fastapi import HTTPException, status
from fastapi.security.base import SecurityBase
from starlette.requests import Request
from starlette.responses import Response
from ..utils.auth import verify_token


class AuthMiddleware:
    """
    Custom authentication middleware to verify JWT tokens.
    This middleware checks for valid JWT tokens in the Authorization header.
    """

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        request = Request(scope)

        # Skip authentication for health check and root endpoints
        if request.url.path in ["/health", "/"]:
            return await self.app(scope, receive, send)

        # For API endpoints, check authentication
        if request.url.path.startswith("/api/"):
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                response = Response(
                    content="Not authenticated",
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    headers={"WWW-Authenticate": "Bearer"}
                )
                return await response(scope, receive, send)

            token = auth_header.split(" ")[1]
            payload = verify_token(token)
            if not payload:
                response = Response(
                    content="Could not validate credentials",
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    headers={"WWW-Authenticate": "Bearer"}
                )
                return await response(scope, receive, send)

        return await self.app(scope, receive, send)