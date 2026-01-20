from sqlmodel import SQLModel, Field
from datetime import datetime
import uuid

class User(SQLModel, table=True):
    __tablename__ = "users"

    user_id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    name: str = Field(max_length=255)
    email: str = Field(unique=True, index=True, max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)
