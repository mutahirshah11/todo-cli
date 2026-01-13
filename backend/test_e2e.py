"""
End-to-End Test Suite for Database Persistence Feature
Validates all user stories and requirements are satisfied
"""

import asyncio
import os
import uuid
import pytest
from datetime import datetime
from sqlmodel import create_engine, select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import sys

# Import our models and repositories
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from api.models.database import Task, User
from api.repositories.task_repository import TaskRepository
from api.repositories.user_repository import UserRepository
from api.validation.task_validation import TaskValidationRules


async def test_user_story_1_persistent_task_storage():
    """
    Test User Story 1: Persistent Task Storage
    As an authenticated user, I want my tasks to be stored permanently
    so that they remain available after application restarts and system failures.
    """
    print("Testing User Story 1: Persistent Task Storage...")

    # Get database URL
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        pytest.skip("DATABASE_URL not set")

    # Create async engine and session
    async_engine = create_async_engine(database_url)
    async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

    # Create a test user
    user_id = str(uuid.uuid4())
    test_user_email = f"user_story_1_test_{int(datetime.now().timestamp())}@example.com"

    async with async_session() as session:
        # Create user
        user_repo = UserRepository(session)
        user = await user_repo.create_user(test_user_email)
        user_id = user.user_id
        await session.commit()
        print(f"Created test user: {user_id}")

        # Create task repository
        task_repo = TaskRepository(session)

        # Create multiple test tasks
        test_tasks_data = [
            {"title": "Persistent Task 1", "description": "First persistent task", "completed": False},
            {"title": "Persistent Task 2", "description": "Second persistent task", "completed": True},
            {"title": "Persistent Task 3", "description": "Third persistent task", "completed": False},
        ]

        created_tasks = []
        for task_data in test_tasks_data:
            task = await task_repo.create_task(
                title=task_data["title"],
                description=task_data["description"],
                is_completed=task_data["completed"],
                user_id=user_id
            )
            created_tasks.append(task)
            print(f"Created task: {task.id} - {task.title}")

        # Verify all tasks were created
        assert len(created_tasks) == 3, f"Expected 3 tasks, got {len(created_tasks)}"

        # Retrieve tasks to verify persistence
        retrieved_tasks = await task_repo.get_tasks_by_user(user_id)
        assert len(retrieved_tasks) == 3, f"Expected 3 persisted tasks, got {len(retrieved_tasks)}"

        # Verify task details
        for i, task in enumerate(retrieved_tasks):
            assert task.title == test_tasks_data[i]["title"], f"Task {i} title mismatch"
            assert task.description == test_tasks_data[i]["description"], f"Task {i} description mismatch"
            assert task.is_completed == test_tasks_data[i]["completed"], f"Task {i} completion status mismatch"
            assert task.user_id == user_id, f"Task {i} user_id mismatch"
            print(f"✓ Verified task persistence: {task.title}")

    # Clean up
    await async_engine.dispose()

    print("✓ User Story 1 tests PASSED")
    return True


async def test_user_story_2_user_task_ownership():
    """
    Test User Story 2: User-Task Ownership Relationship
    As an authenticated user, I want my tasks to be securely associated
    with my account so that no other user can access, modify, or delete my tasks.
    """
    print("\nTesting User Story 2: User-Task Ownership...")

    # Get database URL
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        pytest.skip("DATABASE_URL not set")

    # Create async engine and session
    async_engine = create_async_engine(database_url)
    async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

    # Create two test users
    user1_id = str(uuid.uuid4())
    user2_id = str(uuid.uuid4())
    user1_email = f"user1_test_{int(datetime.now().timestamp())}@example.com"
    user2_email = f"user2_test_{int(datetime.now().timestamp())}@example.com"

    async with async_session() as session:
        # Create users
        user_repo = UserRepository(session)

        user1 = await user_repo.create_user(user1_email)
        user1_id = user1.user_id

        user2 = await user_repo.create_user(user2_email)
        user2_id = user2.user_id

        await session.commit()
        print(f"Created users: {user1_id} and {user2_id}")

        # Create task repository
        task_repo = TaskRepository(session)

        # User 1 creates tasks
        user1_task1 = await task_repo.create_task(
            title="User 1 Task 1",
            description="Owned by user 1",
            is_completed=False,
            user_id=user1_id
        )

        user1_task2 = await task_repo.create_task(
            title="User 1 Task 2",
            description="Also owned by user 1",
            is_completed=True,
            user_id=user1_id
        )

        # User 2 creates tasks
        user2_task1 = await task_repo.create_task(
            title="User 2 Task 1",
            description="Owned by user 2",
            is_completed=False,
            user_id=user2_id
        )

        await session.commit()
        print("Created tasks for both users")

        # Verify User 1 can only see their own tasks
        user1_tasks = await task_repo.get_tasks_by_user(user1_id)
        assert len(user1_tasks) == 2, f"User 1 should have 2 tasks, got {len(user1_tasks)}"
        for task in user1_tasks:
            assert task.user_id == user1_id, f"User 1 retrieved task belonging to another user: {task.user_id}"
        print(f"✓ User 1 can access {len(user1_tasks)} of their own tasks")

        # Verify User 2 can only see their own tasks
        user2_tasks = await task_repo.get_tasks_by_user(user2_id)
        assert len(user2_tasks) == 1, f"User 2 should have 1 task, got {len(user2_tasks)}"
        for task in user2_tasks:
            assert task.user_id == user2_id, f"User 2 retrieved task belonging to another user: {task.user_id}"
        print(f"✓ User 2 can access {len(user2_tasks)} of their own tasks")

        # Test ownership verification
        user1_can_access_task1 = await task_repo.verify_task_ownership(user1_task1.id, user1_id)
        user1_can_access_task2 = await task_repo.verify_task_ownership(user1_task2.id, user1_id)
        user2_cannot_access_user1_task = not await task_repo.verify_task_ownership(user1_task1.id, user2_id)

        assert user1_can_access_task1, "User 1 should own their own task"
        assert user1_can_access_task2, "User 1 should own their own task"
        assert user2_cannot_access_user1_task, "User 2 should not own User 1's task"
        print("✓ Ownership verification working correctly")

        # Test that users cannot modify each other's tasks
        # Attempt to update User 1's task with User 2's context (should fail)
        original_title = user1_task1.title
        try:
            updated_task = await task_repo.update_task(
                task_id=user1_task1.id,
                user_id=user2_id,  # Wrong user trying to update
                title="Attempted modification by wrong user"
            )
            # If we get here, the update succeeded when it shouldn't have
            assert updated_task is None, "User 2 should not be able to update User 1's task"
        except:
            # This is expected - the update should fail
            pass

        # Verify original task is unchanged
        refreshed_task = await task_repo.get_task_by_id(user1_task1.id, user1_id)
        assert refreshed_task.title == original_title, "Original task should remain unchanged"
        print("✓ Cross-user modification protection working")

    # Clean up
    await async_engine.dispose()

    print("✓ User Story 2 tests PASSED")
    return True


async def test_user_story_3_consistent_behavior():
    """
    Test User Story 3: Consistent Task Behavior
    As an authenticated user, I want the task management behavior to remain
    consistent with the existing Python console application.
    """
    print("\nTesting User Story 3: Consistent Task Behavior...")

    # Get database URL
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        pytest.skip("DATABASE_URL not set")

    # Create async engine and session
    async_engine = create_async_engine(database_url)
    async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

    # Create a test user
    user_id = str(uuid.uuid4())
    test_user_email = f"user_story_3_test_{int(datetime.now().timestamp())}@example.com"

    async with async_session() as session:
        # Create user
        user_repo = UserRepository(session)
        user = await user_repo.create_user(test_user_email)
        user_id = user.user_id
        await session.commit()
        print(f"Created test user: {user_id}")

        # Create task repository
        task_repo = TaskRepository(session)

        # Test validation rules matching console app behavior
        validation_rules = TaskValidationRules()

        # Test title validation (same as console app)
        valid_title = "Valid Task Title"
        validated_title = validation_rules.validate_title(valid_title)
        assert validated_title == valid_title, "Title validation should pass for valid titles"
        print("✓ Title validation matches console app behavior")

        # Test description validation (same as console app)
        valid_description = "Valid task description"
        validated_description = validation_rules.validate_description(valid_description)
        assert validated_description == valid_description.strip(), "Description validation should pass"
        print("✓ Description validation matches console app behavior")

        # Test length limits (same as console app)
        long_title = "x" * 101  # Should exceed limit
        try:
            validation_rules.validate_title(long_title)
            assert False, "Long title should fail validation"
        except ValueError:
            print("✓ Title length validation matches console app behavior")

        long_description = "x" * 501  # Should exceed limit
        try:
            validation_rules.validate_description(long_description)
            assert False, "Long description should fail validation"
        except ValueError:
            print("✓ Description length validation matches console app behavior")

        # Test completion status validation (same as console app)
        validated_completed = validation_rules.validate_completed(False)
        assert validated_completed is False, "Boolean validation should pass"
        print("✓ Completion status validation matches console app behavior")

        # Test task creation with validation
        test_task = await task_repo.create_task(
            title="Console-Compatible Task",
            description="Task created with console-compatible validation",
            is_completed=False,
            user_id=user_id
        )
        assert test_task.title == "Console-Compatible Task", "Task should be created successfully"
        print("✓ Task creation with validation works")

        # Test task update (matches console app behavior)
        updated_task = await task_repo.update_task(
            task_id=test_task.id,
            user_id=user_id,
            title="Updated Console-Compatible Task",
            description="Updated description",
            is_completed=True
        )
        assert updated_task.title == "Updated Console-Compatible Task", "Task should be updated successfully"
        assert updated_task.is_completed is True, "Completion status should be updated"
        print("✓ Task update behavior matches console app")

        # Test completion toggle (matches console app behavior)
        toggled_task = await task_repo.toggle_task_completion(test_task.id, user_id, False)
        assert toggled_task.is_completed is False, "Completion status should be toggled to False"
        print("✓ Task completion toggle matches console app behavior")

    # Clean up
    await async_engine.dispose()

    print("✓ User Story 3 tests PASSED")
    return True


async def test_performance_requirements():
    """
    Test that performance requirements are met.
    """
    print("\nTesting Performance Requirements...")

    # Get database URL
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        pytest.skip("DATABASE_URL not set")

    # Create async engine and session
    async_engine = create_async_engine(database_url)
    async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

    # Create a test user
    user_id = str(uuid.uuid4())
    test_user_email = f"perf_test_{int(datetime.now().timestamp())}@example.com"

    async with async_session() as session:
        # Create user
        user_repo = UserRepository(session)
        user = await user_repo.create_user(test_user_email)
        user_id = user.user_id
        await session.commit()
        print(f"Created test user: {user_id}")

        # Create task repository
        task_repo = TaskRepository(session)

        # Test basic performance with a reasonable number of tasks
        import time
        start_time = time.time()

        # Create 100 tasks
        for i in range(100):
            await task_repo.create_task(
                title=f"Performance Test Task {i+1}",
                description=f"Task #{i+1} for performance testing",
                is_completed=(i % 2 == 0),
                user_id=user_id
            )

        creation_time = time.time() - start_time
        print(f"Created 100 tasks in {creation_time:.2f} seconds")

        # Retrieve all tasks
        retrieval_start = time.time()
        tasks = await task_repo.get_tasks_by_user(user_id)
        retrieval_time = time.time() - retrieval_start

        assert len(tasks) == 100, f"Expected 100 tasks, got {len(tasks)}"
        print(f"Retrieved 100 tasks in {retrieval_time:.2f} seconds")

        # Test that retrieval is reasonably fast
        assert retrieval_time < 2.0, f"Retrieval of 100 tasks took too long: {retrieval_time}s"
        print("✓ Performance requirements met")

    # Clean up
    await async_engine.dispose()

    print("✓ Performance tests PASSED")
    return True


async def main():
    """
    Main test function to run all end-to-end tests.
    """
    print("Starting End-to-End Tests for Database Persistence Feature...")
    print("="*70)

    # Run all tests
    test_results = []

    test_results.append(await test_user_story_1_persistent_task_storage())
    test_results.append(await test_user_story_2_user_task_ownership())
    test_results.append(await test_user_story_3_consistent_behavior())
    test_results.append(await test_performance_requirements())

    print("\n" + "="*70)
    if all(test_results):
        print("✓ ALL END-TO-END TESTS PASSED")
        print("Database persistence feature is fully functional and meets all requirements!")
        return True
    else:
        print("✗ SOME END-TO-END TESTS FAILED")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)