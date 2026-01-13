"""
Test script to verify database connection and session management functionality
"""
import asyncio
import os
from api.database.session import AsyncSessionLocal, test_connection
from api.models.database import User, Task
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_database_connection():
    """
    Test the database connection and session management functionality.
    """
    print("Testing database connection...")

    try:
        # Test basic connection
        success = await test_connection()
        if success:
            print("✓ Basic database connection test passed")
        else:
            print("✗ Basic database connection test failed")
            return False

        # Test creating a session and performing basic operations
        print("\nTesting session management...")
        async with AsyncSessionLocal() as session:
            # Try to create a simple query
            result = await session.execute("SELECT 1 as test")
            row = result.fetchone()

            if row and row.test == 1:
                print("✓ Session management test passed")
            else:
                print("✗ Session management test failed")
                return False

        print("\n✓ All database connection and session management tests passed!")
        return True

    except Exception as e:
        print(f"✗ Database connection test failed: {e}")
        return False


async def test_models_creation():
    """
    Test that the SQLModel models are properly defined.
    """
    print("\nTesting model definitions...")

    try:
        # Test creating model instances (without saving to database)
        user = User(
            email="test@example.com",
            is_active=True
        )

        task = Task(
            title="Test Task",
            description="Test Description",
            is_completed=False,
            user_id=user.user_id  # This will use the default factory
        )

        print("✓ Model definitions test passed")
        return True

    except Exception as e:
        print(f"✗ Model definitions test failed: {e}")
        return False


async def run_all_tests():
    """
    Run all database tests.
    """
    print("Running database connection and session management tests...\n")

    connection_success = await test_database_connection()
    models_success = await test_models_creation()

    if connection_success and models_success:
        print("\n🎉 All tests passed! Database integration is working correctly.")
        return True
    else:
        print("\n❌ Some tests failed. Please check the database configuration.")
        return False


if __name__ == "__main__":
    # Run the tests
    success = asyncio.run(run_all_tests())

    if success:
        print("\nDatabase integration verification: PASSED")
    else:
        print("\nDatabase integration verification: FAILED")