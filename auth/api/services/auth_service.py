from datetime import timedelta
from typing import Optional
from fastapi import HTTPException, status
import uuid
from datetime import datetime

from ..models.user import UserCreate, UserInDB, UserPublic
from ..utils.jwt import get_password_hash, verify_password, create_access_token
from ..exceptions.auth_exceptions import UserAlreadyExistsException, InvalidCredentialsException


class MockUserService:
    """
    Mock user service for demonstration purposes.
    In a real implementation, this would interact with a database.
    """

    def __init__(self):
        self.users_db = {}  # In-memory storage for demo
        # Add demo credentials for temporary use
        self._add_demo_user()

    def _add_demo_user(self):
        """Add a demo user for temporary access until database integration."""
        from ..utils.jwt import get_password_hash
        import uuid
        from datetime import datetime

        demo_user_id = "demo-user-123"
        demo_email = "demo@example.com"
        demo_password = "DemoPass123!"
        demo_password_hash = get_password_hash(demo_password)

        demo_user = UserInDB(
            id=demo_user_id,
            email=demo_email,
            password_hash=demo_password_hash,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            is_active=True
        )

        self.users_db[demo_user_id] = demo_user
        print(f"Demo user created: {demo_email}")
        print(f"Demo credentials - Email: {demo_email}, Password: {demo_password}")

    def get_user_by_email(self, email: str) -> Optional[UserInDB]:
        """Get a user by email."""
        for user in self.users_db.values():
            if user.email == email:
                return user
        return None

    def get_user_by_id(self, user_id: str) -> Optional[UserInDB]:
        """Get a user by ID."""
        return self.users_db.get(user_id)

    def create_user(self, user_create: UserCreate) -> UserInDB:
        """Create a new user."""
        # Check if user already exists
        existing_user = self.get_user_by_email(user_create.email)
        if existing_user:
            raise UserAlreadyExistsException(f"User with email {user_create.email} already exists")

        # Create new user
        user_id = str(uuid.uuid4())
        password_hash = get_password_hash(user_create.password)
        user = UserInDB(
            id=user_id,
            email=user_create.email,
            password_hash=password_hash,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            is_active=True
        )

        self.users_db[user_id] = user
        return user


class AuthService:
    def __init__(self):
        self.user_service = MockUserService()

    def register_user(self, user_create: UserCreate) -> tuple[UserPublic, str]:
        """Register a new user and return user data with access token."""
        # Create user
        user_in_db = self.user_service.create_user(user_create)

        # Create access token
        token_data = {"sub": user_in_db.id, "email": user_in_db.email}
        access_token = create_access_token(data=token_data)

        # Convert to public user model
        user_public = UserPublic(
            id=user_in_db.id,
            email=user_in_db.email,
            created_at=user_in_db.created_at,
            updated_at=user_in_db.updated_at,
            is_active=user_in_db.is_active
        )

        return user_public, access_token

    def authenticate_user(self, email: str, password: str) -> tuple[UserPublic, str]:
        """Authenticate user and return user data with access token."""
        user = self.user_service.get_user_by_email(email)

        if not user or not verify_password(password, user.password_hash):
            raise InvalidCredentialsException("Invalid email or password")

        if not user.is_active:
            raise InvalidCredentialsException("User account is deactivated")

        # Create access token
        token_data = {"sub": user.id, "email": user.email}
        access_token = create_access_token(data=token_data)

        # Convert to public user model
        user_public = UserPublic(
            id=user.id,
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
            id=user.id,
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
            id=user.id,
            email=user.email,
            created_at=user.created_at,
            updated_at=user.updated_at,
            is_active=user.is_active
        )

        return user_public