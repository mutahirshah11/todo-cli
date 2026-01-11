from pydantic import BaseModel
from typing import Optional


class ErrorResponse(BaseModel):
    """Standard error response model."""
    error: str
    error_code: Optional[int] = None