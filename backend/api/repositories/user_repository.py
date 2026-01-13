from typing import Optional
from sqlmodel import select
from sqlalchemy.exc import IntegrityError
from ..models.database import User
from ..database.session import DatabaseErrorHandler
from datetime import datetime


class UserRepository:
    """
    Repository class for handling User database operations.
    Implements CRUD operations for users with proper error handling.
    """

    def __init__(self, session):
        """
        Initialize the UserRepository with a database session.

        Args:
            session: Async database session from SQLModel
        """
        self.session = session
        self.error_handler = DatabaseErrorHandler()

    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        """
        Retrieve a user by their ID.

        Args:
            user_id: The ID of the user to retrieve

        Returns:
            User object if found, None otherwise
        """
        try:
            statement = select(User).where(User.user_id == user_id)
            result = await self.session.execute(statement)
            return result.scalar_one_or_none()
        except Exception as e:
            self.error_handler.handle_database_error(e, "Getting user by ID")
            raise

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Retrieve a user by their email address.

        Args:
            email: The email address of the user to retrieve

        Returns:
            User object if found, None otherwise
        """
        try:
            statement = select(User).where(User.email == email)
            result = await self.session.execute(statement)
            return result.scalar_one_or_none()
        except Exception as e:
            self.error_handler.handle_database_error(e, "Getting user by email")
            raise

    async def create_user(self, email: str) -> User:
        """
        Create a new user.

        Args:
            email: Email address of the new user

        Returns:
            Created User object
        """
        try:
            db_user = User(
                email=email,
                is_active=True
            )

            self.session.add(db_user)
            await self.session.commit()
            await self.session.refresh(db_user)
            return db_user
        except IntegrityError as e:
            self.error_handler.handle_database_error(e, "Creating user - integrity constraint violation (email might already exist)")
            raise
        except Exception as e:
            self.error_handler.handle_database_error(e, "Creating user")
            raise

    async def update_user(self, user_id: str, email: Optional[str] = None,
                         is_active: Optional[bool] = None) -> Optional[User]:
        """
        Update an existing user.

        Args:
            user_id: ID of the user to update
            email: New email address (optional)
            is_active: New active status (optional)

        Returns:
            Updated User object if successful, None if user not found
        """
        try:
            # First, get the existing user
            statement = select(User).where(User.user_id == user_id)
            result = await self.session.execute(statement)
            db_user = result.scalar_one_or_none()

            if not db_user:
                return None

            # Update fields if provided
            if email is not None:
                db_user.email = email
            if is_active is not None:
                db_user.is_active = is_active

            db_user.updated_at = datetime.utcnow()

            await self.session.commit()
            await self.session.refresh(db_user)
            return db_user
        except IntegrityError as e:
            self.error_handler.handle_database_error(e, "Updating user - integrity constraint violation")
            raise
        except Exception as e:
            self.error_handler.handle_database_error(e, "Updating user")
            raise

    async def delete_user(self, user_id: str) -> bool:
        """
        Delete a user by their ID.

        Args:
            user_id: ID of the user to delete

        Returns:
            True if user was deleted, False if not found
        """
        try:
            # Note: This will fail if there are tasks associated with this user due to foreign key constraint
            # In a real application, you'd want to either cascade delete the user's tasks or handle this differently
            from sqlmodel import delete
            statement = delete(User).where(User.user_id == user_id)
            result = await self.session.execute(statement)

            if result.rowcount > 0:
                await self.session.commit()
                return True
            else:
                return False
        except Exception as e:
            self.error_handler.handle_database_error(e, "Deleting user")
            raise

    async def deactivate_user(self, user_id: str) -> Optional[User]:
        """
        Deactivate a user account (soft delete approach).

        Args:
            user_id: ID of the user to deactivate

        Returns:
            Updated User object if successful, None if user not found
        """
        try:
            statement = select(User).where(User.user_id == user_id)
            result = await self.session.execute(statement)
            db_user = result.scalar_one_or_none()

            if not db_user:
                return None

            db_user.is_active = False
            db_user.updated_at = datetime.utcnow()

            await self.session.commit()
            await self.session.refresh(db_user)
            return db_user
        except Exception as e:
            self.error_handler.handle_database_error(e, "Deactivating user")
            raise

    async def activate_user(self, user_id: str) -> Optional[User]:
        """
        Activate a user account.

        Args:
            user_id: ID of the user to activate

        Returns:
            Updated User object if successful, None if user not found
        """
        try:
            statement = select(User).where(User.user_id == user_id)
            result = await self.session.execute(statement)
            db_user = result.scalar_one_or_none()

            if not db_user:
                return None

            db_user.is_active = True
            db_user.updated_at = datetime.utcnow()

            await self.session.commit()
            await self.session.refresh(db_user)
            return db_user
        except Exception as e:
            self.error_handler.handle_database_error(e, "Activating user")
            raise

    async def user_exists(self, user_id: str) -> bool:
        """
        Check if a user exists by their ID.

        Args:
            user_id: ID of the user to check

        Returns:
            True if user exists, False otherwise
        """
        try:
            statement = select(User).where(User.user_id == user_id)
            result = await self.session.execute(statement)
            return result.scalar_one_or_none() is not None
        except Exception as e:
            self.error_handler.handle_database_error(e, "Checking if user exists")
            raise

    async def user_exists_by_email(self, email: str) -> bool:
        """
        Check if a user exists by their email.

        Args:
            email: Email address to check

        Returns:
            True if user exists, False otherwise
        """
        try:
            statement = select(User).where(User.email == email)
            result = await self.session.execute(statement)
            return result.scalar_one_or_none() is not None
        except Exception as e:
            self.error_handler.handle_database_error(e, "Checking if user exists by email")
            raise