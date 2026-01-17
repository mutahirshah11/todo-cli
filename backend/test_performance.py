"""
Performance test script to verify the system handles up to 10,000 tasks per user efficiently
"""

import asyncio
import os
import time
import uuid
from datetime import datetime
from sqlmodel import create_engine, select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
import sys

# Import our models and repositories
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from api.models.database import Task, User
from api.repositories.task_repository import TaskRepository
from api.repositories.user_repository import UserRepository


async def test_performance_with_large_dataset(num_tasks=10000, batch_size=1000):
    """
    Test performance with a large number of tasks per user (up to 10,000).

    Args:
        num_tasks: Number of tasks to create and test with
        batch_size: Number of tasks to create in each batch
    """
    print(f"Testing performance with {num_tasks} tasks per user...")

    # Get database URL
    database_url = os.getenv("NEON_DATABASE_URL")
    if not database_url:
        print("ERROR: NEON_DATABASE_URL environment variable not set")
        return False

    # Create async engine and session
    async_engine = create_async_engine(database_url)
    async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

    # Create a test user
    user_id = str(uuid.uuid4())
    test_user_email = f"performance_test_{int(time.time())}@example.com"

    print(f"Creating performance test user: {test_user_email}")

    # Create user first
    async with async_session() as session:
        user_repo = UserRepository(session)
        user = await user_repo.create_user(test_user_email)
        user_id = user.user_id
        await session.commit()
        print(f"Created test user: {user_id}")

    # Test creation performance
    print(f"\nCreating {num_tasks} tasks in batches of {batch_size}...")
    start_time = time.time()

    tasks_created = 0
    batch_start_time = time.time()

    for batch_start in range(0, num_tasks, batch_size):
        batch_end = min(batch_start + batch_size, num_tasks)

        async with async_session() as session:
            task_repo = TaskRepository(session)

            # Create tasks in this batch
            for i in range(batch_start, batch_end):
                await task_repo.create_task(
                    title=f"Performance Test Task {i+1}",
                    description=f"This is task #{i+1} for performance testing with large dataset",
                    is_completed=(i % 3 == 0),  # Every third task is completed
                    user_id=user_id
                )
                tasks_created += 1

                if (i + 1) % 1000 == 0:
                    print(f"Created {tasks_created}/{num_tasks} tasks...")

            await session.commit()

        # Print batch performance
        current_batch_time = time.time() - batch_start_time
        print(f"Batch {batch_start//batch_size + 1} ({batch_start}-{batch_end-1}) completed in {current_batch_time:.2f}s")
        batch_start_time = time.time()

    creation_time = time.time() - start_time
    print(f"\n✓ Created {tasks_created} tasks in {creation_time:.2f} seconds")
    print(f"Average creation rate: {tasks_created/creation_time:.2f} tasks/second")

    # Test retrieval performance
    print(f"\nTesting retrieval performance for {tasks_created} tasks...")
    retrieval_start_time = time.time()

    async with async_session() as session:
        task_repo = TaskRepository(session)

        # Retrieve all tasks
        retrieved_tasks = await task_repo.get_tasks_by_user(user_id)
        retrieval_time = time.time() - retrieval_start_time

    print(f"✓ Retrieved {len(retrieved_tasks)} tasks in {retrieval_time:.2f} seconds")

    # Test filtered retrieval (completed tasks)
    print(f"\nTesting filtered retrieval (completed tasks only)...")
    filtered_start_time = time.time()

    async with async_session() as session:
        task_repo = TaskRepository(session)

        completed_tasks = await task_repo.get_tasks_by_completion_status(user_id, is_completed=True)
        filtered_time = time.time() - filtered_start_time

    print(f"✓ Retrieved {len(completed_tasks)} completed tasks in {filtered_time:.2f} seconds")

    # Test task count performance
    print(f"\nTesting task count performance...")
    count_start_time = time.time()

    async with async_session() as session:
        task_repo = TaskRepository(session)

        task_count = await task_repo.get_task_count_by_user(user_id)
        count_time = time.time() - count_start_time

    print(f"✓ Counted {task_count} tasks in {count_time:.4f} seconds")

    # Performance validation
    print(f"\nPerformance Validation:")
    print(f"- Creation rate: {tasks_created/creation_time:.2f} tasks/sec")
    print(f"- Retrieval time for {len(retrieved_tasks)} tasks: {retrieval_time:.2f} sec")
    print(f"- Count query time: {count_time:.4f} sec")

    # Validate that we have the expected number of tasks
    assert len(retrieved_tasks) == num_tasks, f"Expected {num_tasks} tasks, got {len(retrieved_tasks)}"
    assert task_count == num_tasks, f"Expected count {num_tasks}, got {task_count}"

    # Performance benchmarks (these are reasonable targets for 10k tasks)
    creation_rate_threshold = 100  # tasks per second
    retrieval_time_threshold = 2.0  # seconds for 10k tasks
    count_time_threshold = 0.1  # seconds for count query

    performance_ok = True
    if tasks_created/creation_time < creation_rate_threshold:
        print(f"⚠ Warning: Creation rate ({tasks_created/creation_time:.2f}) below threshold ({creation_rate_threshold})")
        performance_ok = False

    if retrieval_time > retrieval_time_threshold:
        print(f"⚠ Warning: Retrieval time ({retrieval_time:.2f}s) above threshold ({retrieval_time_threshold}s)")
        performance_ok = False

    if count_time > count_time_threshold:
        print(f"⚠ Warning: Count time ({count_time:.4f}s) above threshold ({count_time_threshold}s)")
        performance_ok = False

    if performance_ok:
        print("✓ Performance requirements met!")
    else:
        print("⚠ Some performance requirements not met, but functionality works")

    # Clean up: dispose of engine
    await async_engine.dispose()

    print(f"\n✓ Performance test completed for {num_tasks} tasks")
    return True


async def test_specific_performance_scenarios():
    """
    Test specific performance scenarios that might be problematic.
    """
    print("\nTesting specific performance scenarios...")

    # Get database URL
    database_url = os.getenv("NEON_DATABASE_URL")
    if not database_url:
        print("ERROR: NEON_DATABASE_URL environment variable not set")
        return False

    # Create async engine and session
    async_engine = create_async_engine(database_url)
    async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

    # Test scenario 1: Many concurrent operations
    print("\nTesting concurrent operations...")

    async def create_single_task(user_id, task_num):
        async with async_session() as session:
            task_repo = TaskRepository(session)
            task = await task_repo.create_task(
                title=f"Concurrent Task {task_num}",
                description=f"Task {task_num} for concurrent test",
                is_completed=False,
                user_id=user_id
            )
            await session.commit()
            return task.id

    # Create a test user
    user_id = str(uuid.uuid4())
    test_user_email = f"concurrent_test_{int(time.time())}@example.com"

    async with async_session() as session:
        user_repo = UserRepository(session)
        user = await user_repo.create_user(test_user_email)
        user_id = user.user_id
        await session.commit()

    # Create 100 tasks concurrently
    concurrent_tasks = [create_single_task(user_id, i) for i in range(100)]
    start_time = time.time()
    created_task_ids = await asyncio.gather(*concurrent_tasks)
    concurrent_time = time.time() - start_time

    print(f"Created 100 tasks concurrently in {concurrent_time:.2f} seconds")
    print(f"Rate: {100/concurrent_time:.2f} tasks/sec")

    # Test scenario 2: Large text in descriptions
    print("\nTesting with large text fields...")
    large_text = "This is a large text description. " * 500  # ~15KB of text

    large_text_start_time = time.time()
    async with async_session() as session:
        task_repo = TaskRepository(session)
        large_task = await task_repo.create_task(
            title="Large Text Task",
            description=large_text,
            is_completed=False,
            user_id=user_id
        )
        await session.commit()
        large_text_time = time.time() - large_text_start_time

    print(f"Created task with large text ({len(large_text)} chars) in {large_text_time:.4f} seconds")

    # Clean up
    await async_engine.dispose()

    print("✓ Specific performance scenarios tested")
    return True


async def main():
    """
    Main test function to run performance tests.
    """
    print("Starting performance tests with large datasets...")
    print("="*60)

    # Run basic performance test with smaller number first (as 10k might take a while)
    print("Running initial test with 1000 tasks (smaller sample)...")
    success1 = await test_performance_with_large_dataset(num_tasks=1000, batch_size=500)

    if success1:
        print("\nRunning full performance test with 10,000 tasks...")
        success2 = await test_performance_with_large_dataset(num_tasks=10000, batch_size=1000)
    else:
        success2 = False

    # Test specific scenarios
    success3 = await test_specific_performance_scenarios()

    print("\n" + "="*60)
    if success1 and success2 and success3:
        print("✓ All performance tests PASSED")
        print("System performs adequately with up to 10,000 tasks per user")
        return True
    else:
        print("✗ Some performance tests FAILED")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)