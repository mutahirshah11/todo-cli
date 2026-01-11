"""
Correlation ID middleware for tracking requests across the system.
"""
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    """
    Middleware to add correlation ID to requests for tracing purposes.
    """

    async def dispatch(self, request: Request, call_next):
        # Generate or extract correlation ID
        correlation_id = request.headers.get('X-Correlation-ID') or str(uuid.uuid4())

        # Add to request state
        request.state.correlation_id = correlation_id

        # Add to response headers
        response = await call_next(request)
        response.headers['X-Correlation-ID'] = correlation_id

        return response