"""
Error Handlers Module
Provides consistent error handling and response formatting for the API
"""

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from typing import Union, Dict, Any
import logging
from enum import Enum


class ErrorCode(str, Enum):
    """Enumeration of standardized error codes."""
    VALIDATION_ERROR = "VALIDATION_ERROR"
    NOT_FOUND = "NOT_FOUND"
    UNAUTHORIZED = "UNAUTHORIZED"
    FORBIDDEN = "FORBIDDEN"
    INTERNAL_ERROR = "INTERNAL_ERROR"
    DUPLICATE_RESOURCE = "DUPLICATE_RESOURCE"
    INVALID_INPUT = "INVALID_INPUT"
    RESOURCE_CONFLICT = "RESOURCE_CONFLICT"


class APIErrorResponse:
    """Standardized error response format."""

    @staticmethod
    def create_error_response(
        error_code: ErrorCode,
        message: str,
        details: Union[str, Dict[str, Any]] = None,
        status_code: int = 500
    ) -> Dict[str, Any]:
        """
        Create a standardized error response.

        Args:
            error_code: Standardized error code
            message: Human-readable error message
            details: Additional error details (optional)
            status_code: HTTP status code

        Returns:
            Dictionary with standardized error response format
        """
        error_response = {
            "error": {
                "code": error_code.value,
                "message": message,
                "status_code": status_code
            }
        }

        if details:
            error_response["error"]["details"] = details

        return error_response


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """
    Global handler for HTTP exceptions.

    Args:
        request: FastAPI request object
        exc: HTTPException instance

    Returns:
        JSONResponse with standardized error format
    """
    logging.error(f"HTTP Exception: {exc.status_code} - {exc.detail}")

    # Map HTTP status codes to error codes
    error_code_map = {
        400: ErrorCode.VALIDATION_ERROR,
        401: ErrorCode.UNAUTHORIZED,
        403: ErrorCode.FORBIDDEN,
        404: ErrorCode.NOT_FOUND,
        409: ErrorCode.DUPLICATE_RESOURCE,
        422: ErrorCode.INVALID_INPUT,
    }

    error_code = error_code_map.get(exc.status_code, ErrorCode.INTERNAL_ERROR)

    error_response = APIErrorResponse.create_error_response(
        error_code=error_code,
        message=str(exc.detail),
        status_code=exc.status_code
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=error_response
    )


async def validation_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Global handler for validation exceptions.

    Args:
        request: FastAPI request object
        exc: Exception instance

    Returns:
        JSONResponse with standardized error format
    """
    logging.error(f"Validation Exception: {str(exc)}")

    error_details = None
    if hasattr(exc, 'errors'):
        error_details = exc.errors()

    error_response = APIErrorResponse.create_error_response(
        error_code=ErrorCode.VALIDATION_ERROR,
        message="Validation failed",
        details=error_details,
        status_code=422
    )

    return JSONResponse(
        status_code=422,
        content=error_response
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Global handler for general exceptions.

    Args:
        request: FastAPI request object
        exc: Exception instance

    Returns:
        JSONResponse with standardized error format
    """
    logging.error(f"General Exception: {str(exc)}", exc_info=True)

    # Don't expose internal error details in production
    import os
    debug_mode = os.getenv("DEBUG", "false").lower() == "true"

    error_message = "An internal server error occurred" if not debug_mode else str(exc)

    error_response = APIErrorResponse.create_error_response(
        error_code=ErrorCode.INTERNAL_ERROR,
        message=error_message,
        status_code=500
    )

    if debug_mode:
        error_response["error"]["debug_info"] = {
            "exception_type": type(exc).__name__,
            "exception_message": str(exc)
        }

    return JSONResponse(
        status_code=500,
        content=error_response
    )


def add_error_handlers(app):
    """
    Register error handlers with the FastAPI application.

    Args:
        app: FastAPI application instance
    """
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)

    # Add specific handlers for validation and other common exceptions
    from pydantic import ValidationError
    app.add_exception_handler(ValidationError, validation_exception_handler)

    logging.info("Error handlers registered successfully")


# Enhanced error response models
from pydantic import BaseModel
from typing import Optional, List


class ErrorDetail(BaseModel):
    """Model for error details."""
    loc: Optional[List[str]] = None
    msg: str
    type: str


class ErrorResponseModel(BaseModel):
    """Model for error response format."""
    error: dict


class ValidationErrorResponseModel(ErrorResponseModel):
    """Model for validation error response format."""
    error: dict
    details: Optional[List[ErrorDetail]] = None