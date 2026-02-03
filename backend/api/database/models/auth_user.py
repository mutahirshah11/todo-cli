from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid


class AuthUser(SQLModel, table=True):
    """User model for authentication service with password hash."""

    __tablename__ = "auth_users"

    user_id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    name: str = Field(max_length=255)  # Store user's name
    email: str = Field(unique=True, index=True, max_length=255)
    password_hash: str = Field(max_length=255)  # Store hashed passwords
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)
