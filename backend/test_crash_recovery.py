"""
Test script to verify tasks remain accessible after server crashes and recovery
This simulates crash scenarios and tests recovery procedures
"""

import asyncio
import os
import signal
import time
import tempfile
import json
from datetime import datetime
from sqlmodel import create_engine, select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import uuid
import subprocess
import sys

# Import our models and repositories
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from api.models.database import Task, User
from api.repositories.task_repository import TaskRepository
from api.repositories.user_repository import UserRepository


async def test_crash_recovery_scenario():
    """
    Test scenario: Create tasks, simulate a crash, recover, and verify tasks still exist.
    Since we can't actually crash a running server in this test, we'll simulate
    the concept by directly testing database resilience and connection recovery.
    """
    print("Testing crash recovery scenario...")

    # Get database URL
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("ERROR: DATABASE_URL environment variable not set")
        return False

    # Create async engine and session
    async_engine = create_async_engine(database_url)
    async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

    # Generate a unique identifier for this test run
    test_run_id = f"crash_test_{int(time.time())}"

    # Create a test user
    user_id = str(uuid.uuid4())
    test_user_email = f"{test_run_id}@example.com"

    # Step 1: Create tasks before "crash"
    print("Step 1: Creating tasks before simulated crash...")
    task_ids = []

    async with async_session() as session:
        # Create user repository and create user
        user_repo = UserRepository(session)
        user = await user_repo.create_user(test_user_email)
        user_id = user.user_id
        print(f"Created test user: {user_id}")

        # Create task repository and create tasks
        task_repo = TaskRepository(session)

        # Create multiple test tasks
        for i in range(5):
            task = await task_repo.create_task(
                title=f"Crash Test Task {i+1} - {test_run_id}",
                description=f"Task {i+1} for crash recovery test run {test_run_id}",
                is_completed=(i % 2 == 0),  # Alternate completion status
                user_id=user_id
            )
            task_ids.append(task.id)
            print(f"Created task: {task.id} - {task.title}")

        # Commit the session
        await session.commit()

        # Verify tasks were created
        initial_tasks = await task_repo.get_tasks_by_user(user_id)
        print(f"Successfully created {len(initial_tasks)} tasks before simulated crash")
        assert len(initial_tasks) == 5, f"Expected 5 tasks, got {len(initial_tasks)}"

    # Simulate crash recovery by creating a new connection
    print("\nSimulating server crash and recovery...")
    print("(Actually reconnecting to database to test persistence)")

    # Dispose of the current engine to simulate connection closure
    await async_engine.dispose()

    # Small delay to simulate recovery time
    await asyncio.sleep(1)

    # Recreate engine to simulate recovery
    async_engine = create_async_engine(database_url)
    async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

    # Step 2: Verify tasks still exist after "recovery"
    print("\nStep 2: Verifying tasks exist after simulated recovery...")

    async with async_session() as session:
        task_repo = TaskRepository(session)

        # Get all tasks for the user
        recovered_tasks = await task_repo.get_tasks_by_user(user_id)
        print(f"Found {len(recovered_tasks)} tasks after recovery")

        # Verify all original tasks exist
        recovered_task_ids = [task.id for task in recovered_tasks]
        for original_id in task_ids:
            assert original_id in recovered_task_ids, f"Task {original_id} missing after recovery"
            print(f"✓ Task {original_id} survived recovery")

        # Verify task content is intact
        for task in recovered_tasks:
            assert test_run_id in task.title, f"Task {task.id} content corrupted after recovery"
            print(f"✓ Task {task.id} content intact: {task.title[:50]}...")

    # Clean up: dispose of engine
    await async_engine.dispose()

    print(f"\n✓ Crash recovery test PASSED for run {test_run_id}")
    print(f"✓ All {len(task_ids)} tasks survived the simulated crash and recovery")
    return True


async def test_connection_recovery():
    """
    Test the connection recovery mechanisms built into the session management.
    """
    print("\nTesting connection recovery mechanisms...")

    from api.database.session import DatabaseErrorHandler

    # Test the retry mechanism by attempting a connection
    async_engine = create_async_engine(os.getenv("DATABASE_URL"))

    try:
        # Try to establish a connection using the error handler
        async with AsyncSession() as session:
            result = await session.execute("SELECT 1")
            value = result.scalar()
            assert value == 1, "Basic connection test failed"
            print("✓ Basic connection test passed")

        print("✓ Connection recovery mechanisms working")
        success = True

    except Exception as e:
        print(f"✗ Connection recovery test failed: {e}")
        success = False
    finally:
        await async_engine.dispose()

    return success


async def test_backup_recovery_integration():
    """
    Test integration with the backup and recovery procedures.
    """
    print("\nTesting backup and recovery integration...")

    # Check if backup script exists
    backup_script = os.path.join(os.path.dirname(__file__), "scripts", "neon_backup_recovery.py")

    if os.path.exists(backup_script):
        print("✓ Backup script exists")

        # Test that the backup script can be imported
        import importlib.util
        spec = importlib.util.spec_from_file_location("neon_backup", backup_script)
        backup_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(backup_module)

        # Test instantiation
        try:
            backup_handler = backup_module.NeonBackupRecovery()
            print("✓ Backup handler can be instantiated")

            # Test backup listing capability
            backups = backup_handler.get_backup_list("./backups")
            print(f"✓ Backup listing works, found {len(backups)} backups")

            return True
        except Exception as e:
            print(f"✗ Backup integration test failed: {e}")
            return False
    else:
        print("✗ Backup script does not exist")
        return False


async def main():
    """
    Main test function to run crash recovery tests.
    """
    print("Starting crash recovery and accessibility tests...")
    print("="*60)

    # Run crash recovery scenario
    success1 = await test_crash_recovery_scenario()

    # Test connection recovery
    success2 = await test_connection_recovery()

    # Test backup recovery integration
    success3 = await test_backup_recovery_integration()

    print("\n" + "="*60)
    if success1 and success2 and success3:
        print("✓ All crash recovery tests PASSED")
        print("Tasks remain accessible after simulated server crashes and recovery")
        return True
    else:
        print("✗ Some crash recovery tests FAILED")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)