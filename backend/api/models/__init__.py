# Import all models to make them available for Alembic autogenerate
from .database import User, Task

# Export models for easy importing
__all__ = ["User", "Task"]