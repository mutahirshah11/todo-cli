"""
Centralized exception handlers for the Todo API.
"""
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from .custom import TaskNotFoundError, UserAccessError
from ..models.error import ErrorResponse


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors and return consistent error format."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ErrorResponse(error="Validation error",
                             error_code=status.HTTP_422_UNPROCESSABLE_ENTITY).dict()
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle HTTP exceptions and return consistent error format."""
    error_response = ErrorResponse(error=exc.detail, error_code=exc.status_code)
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.dict()
    )


async def task_not_found_handler(request: Request, exc: TaskNotFoundError):
    """Handle task not found errors."""
    error_response = ErrorResponse(error=str(exc), error_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=error_response.dict()
    )


async def user_access_error_handler(request: Request, exc: UserAccessError):
    """Handle user access errors."""
    error_response = ErrorResponse(error=str(exc), error_code=status.HTTP_403_FORBIDDEN)
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content=error_response.dict()
    )


async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    error_response = ErrorResponse(error="Internal server error",
                                  error_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response.dict()
    )