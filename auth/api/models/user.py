from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str

    @field_validator('name')
    def validate_name(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Name is required and cannot be empty')
        if len(v) > 255:
            raise ValueError('Name must not exceed 255 characters')
        return v.strip()

    @field_validator('password')
    def validate_password(cls, v):
        # Password must be at least 8 characters with mixed case, numbers, and special characters
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')

        has_upper = any(c.isupper() for c in v)
        has_lower = any(c.islower() for c in v)
        has_digit = any(c.isdigit() for c in v)
        has_special = any(not c.isalnum() for c in v)

        if not (has_upper and has_lower and has_digit and has_special):
            raise ValueError('Password must contain uppercase, lowercase, numbers, and special characters')

        return v


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None


class UserInDB(UserBase):
    id: str
    password_hash: str
    created_at: datetime
    updated_at: datetime
    is_active: bool = True

    class Config:
        from_attributes = True


class UserPublic(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime
    is_active: bool

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: str


class LoginRequest(BaseModel):
    email: str
    password: str