from datetime import timedelta
from typing import Optional
from fastapi import HTTPException, status
import uuid
from datetime import datetime
import os
from sqlmodel import SQLModel, create_engine, Session, select
from sqlalchemy.exc import IntegrityError

from ..models.auth_user import AuthUser
from ..models.user import UserCreate, UserPublic
from ..utils.jwt import get_password_hash, verify_password, create_access_token
from ..exceptions.auth_exceptions import UserAlreadyExistsException, InvalidCredentialsException


class DatabaseUserService:
    """
    Database-backed user service.
    Interacts with the shared database using SQLModel.
    """

    def __init__(self):
        # Get database URL from environment
        database_url = os.getenv("NEON_DATABASE_URL")
        if not database_url:
            raise ValueError("NEON_DATABASE_URL environment variable not set")
            
        # Fix for SQLAlchemy 1.4+ which requires 'postgresql://' instead of 'postgres://'
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql://", 1)

        # Create sync engine for auth service
        self.engine = create_engine(database_url, pool_pre_ping=True)

        # Create tables if they don't exist
        SQLModel.metadata.create_all(self.engine)

        # Ensure the name column exists in the auth_users table
        self._ensure_name_column_exists()

    def _ensure_name_column_exists(self):
        """Ensure the name column exists in the auth_users table."""
        from sqlalchemy import inspect, text

        try:
            inspector = inspect(self.engine)
            columns = [col['name'] for col in inspector.get_columns('auth_users')]

            if 'name' not in columns:
                # Add the name column to the table
                with self.engine.connect() as conn:
                    # Add the name column with a default value
                    conn.execute(text("ALTER TABLE auth_users ADD COLUMN name VARCHAR(255) DEFAULT '' NOT NULL"))
                    conn.commit()
        except Exception as e:
            # If the table doesn't exist yet, it will be created with the name column
            # when SQLModel.metadata.create_all() is called
            pass

    def get_user_by_email(self, email: str) -> Optional[AuthUser]:
        """Get a user by email."""
        with Session(self.engine) as session:
            statement = select(AuthUser).where(AuthUser.email == email)
            user = session.exec(statement).first()

            # Handle case where name might be None for existing users
            if user and not user.name:
                user.name = user.email.split('@')[0]  # Use part of email as default name
                # Update the user in the database
                session.add(user)
                session.commit()

            return user

    def get_user_by_id(self, user_id: str) -> Optional[AuthUser]:
        """Get a user by ID."""
        with Session(self.engine) as session:
            statement = select(AuthUser).where(AuthUser.user_id == user_id)
            user = session.exec(statement).first()

            # Handle case where name might be None for existing users
            if user and not user.name:
                user.name = user.email.split('@')[0]  # Use part of email as default name
                # Update the user in the database
                session.add(user)
                session.commit()

            return user

    def create_user(self, user_create: UserCreate) -> AuthUser:
        """Create a new user."""
        with Session(self.engine) as session:
            # Check if user already exists
            existing_user = self.get_user_by_email(user_create.email)
            if existing_user:
                raise UserAlreadyExistsException(f"User with email {user_create.email} already exists")

            # Create new user
            user_id = str(uuid.uuid4())
            password_hash = get_password_hash(user_create.password)

            user = AuthUser(
                user_id=user_id,
                name=user_create.name,
                email=user_create.email,
                password_hash=password_hash,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                is_active=True
            )

            session.add(user)
            session.commit()
            session.refresh(user)

            return user


class AuthService:
    def __init__(self):
        self.user_service = DatabaseUserService()

    def register_user(self, user_create: UserCreate) -> tuple[UserPublic, str]:
        """Register a new user and return user data with access token."""
        # Create user
        user_in_db = self.user_service.create_user(user_create)

        # Create access token
        token_data = {"sub": user_in_db.user_id, "email": user_in_db.email}
        access_token = create_access_token(data=token_data)

        # Convert to public user model
        user_public = UserPublic(
            id=user_in_db.user_id,
            name=user_in_db.name,
            email=user_in_db.email,
            created_at=user_in_db.created_at,
            updated_at=user_in_db.updated_at,
            is_active=user_in_db.is_active
        )

        return user_public, access_token

    def authenticate_user(self, email: str, password: str) -> tuple[UserPublic, str]:
        """Authenticate user and return user data with access token."""
        # Ensure email is stripped of whitespace
        email = email.strip()
        
        user = self.user_service.get_user_by_email(email)

        # Retry logic: If user not found, wait briefly and try again (handles potential DB cold start/glitches)
        if not user:
            import time
            print(f"User not found initially for {email}, retrying in 0.5s...")
            time.sleep(0.5)
            user = self.user_service.get_user_by_email(email)

        if not user:
            print(f"Authentication failed: User not found for email {email}")
            # return specific error for debugging (switch back to generic later)
            raise InvalidCredentialsException("Invalid email (User not found)")
            
        if not verify_password(password, user.password_hash):
            print(f"Authentication failed: Invalid password for user {email}")
             # return specific error for debugging
            raise InvalidCredentialsException("Invalid password")

        if not user.is_active:
            raise InvalidCredentialsException("User account is deactivated")

        # Create access token
        token_data = {"sub": user.user_id, "email": user.email}
        access_token = create_access_token(data=token_data)

        # Convert to public user model
        user_public = UserPublic(
            id=user.user_id,
            name=user.name,
            email=user.email,
            created_at=user.created_at,
            updated_at=user.updated_at,
            is_active=user.is_active
        )

        return user_public, access_token

    def get_current_user(self, token: str) -> UserPublic:
        """Get current user from token."""
        from ..utils.jwt import verify_token

        payload = verify_token(token)
        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user = self.user_service.get_user_by_id(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user_public = UserPublic(
            id=user.user_id,
            name=user.name,
            email=user.email,
            created_at=user.created_at,
            updated_at=user.updated_at,
            is_active=user.is_active
        )

        return user_public

    def get_current_user_from_token_data(self, token_data: dict) -> UserPublic:
        """Get current user from token data (payload)."""
        user_id = token_data.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user = self.user_service.get_user_by_id(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user_public = UserPublic(
            id=user.user_id,
            name=user.name,
            email=user.email,
            created_at=user.created_at,
            updated_at=user.updated_at,
            is_active=user.is_active
        )

        return user_public