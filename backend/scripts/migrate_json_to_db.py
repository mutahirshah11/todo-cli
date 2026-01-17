"""
Data Migration Script: JSON to Database
This script migrates existing tasks from JSON files to the PostgreSQL database
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from typing import List, Dict, Any
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy import create_engine as sync_create_engine
from sqlalchemy.orm import sessionmaker
import uuid

# Add the backend directory to the path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from api.models.database import Task, User
from api.repositories.user_repository import UserRepository
from api.repositories.task_repository import TaskRepository


class JSONToDBMigration:
    """
    Handles migration of data from JSON files to PostgreSQL database.
    """

    def __init__(self, database_url: str = None):
        """
        Initialize the migration handler.

        Args:
            database_url: PostgreSQL database URL. If not provided, uses NEON_DATABASE_URL environment variable.
        """
        self.database_url = database_url or os.getenv("NEON_DATABASE_URL")
        if not self.database_url:
            raise ValueError("NEON_DATABASE_URL must be provided either as parameter or environment variable")

        # Create synchronous engine for migration
        self.sync_engine = sync_create_engine(self.database_url)
        self.SessionLocal = sessionmaker(bind=self.sync_engine)

    def load_json_data(self, json_file_path: str) -> List[Dict[str, Any]]:
        """
        Load data from JSON file.

        Args:
            json_file_path: Path to the JSON file to load

        Returns:
            List of dictionaries containing the JSON data
        """
        if not os.path.exists(json_file_path):
            print(f"Warning: JSON file {json_file_path} does not exist. Skipping migration.")
            return []

        with open(json_file_path, 'r', encoding='utf-8') as file:
            try:
                data = json.load(file)
                if isinstance(data, list):
                    return data
                else:
                    print(f"Warning: JSON file {json_file_path} does not contain an array. Skipping migration.")
                    return []
            except json.JSONDecodeError as e:
                print(f"Error: Invalid JSON in {json_file_path}: {e}")
                return []

    def migrate_tasks(self, json_file_path: str = "todo_data.json") -> Dict[str, int]:
        """
        Migrate tasks from JSON file to database.

        Args:
            json_file_path: Path to the JSON file containing tasks

        Returns:
            Dictionary with migration statistics
        """
        json_tasks = self.load_json_data(json_file_path)

        if not json_tasks:
            print("No tasks to migrate from JSON file.")
            return {"total_processed": 0, "migrated": 0, "skipped": 0, "errors": 0}

        stats = {
            "total_processed": len(json_tasks),
            "migrated": 0,
            "skipped": 0,
            "errors": 0
        }

        print(f"Starting migration of {len(json_tasks)} tasks from {json_file_path}")

        for json_task in json_tasks:
            try:
                # Create or get user based on user_id from JSON
                user_id = json_task.get('user_id', str(uuid.uuid4()))

                with self.SessionLocal() as session:
                    # Check if user exists, create if not
                    user_repo = UserRepository(session)
                    existing_user = user_repo.get_user_by_id_sync(user_id)

                    if not existing_user:
                        # Create new user
                        email = f"user_{user_id}@example.com"  # Default email if not provided
                        user = User(
                            user_id=user_id,
                            email=email,
                            is_active=True
                        )
                        session.add(user)
                        session.commit()
                        print(f"Created user: {user_id}")

                    # Check if task already exists in database
                    # Try to find if task with same title and user exists
                    from sqlalchemy import select
                    existing_task_stmt = select(Task).where(
                        Task.title == json_task.get('title'),
                        Task.user_id == user_id
                    )
                    result = session.execute(existing_task_stmt)
                    existing_task = result.scalar_one_or_none()

                    if existing_task:
                        print(f"Task '{json_task.get('title')}' for user {user_id} already exists. Skipping.")
                        stats["skipped"] += 1
                        continue

                    # Create new task from JSON data
                    task = Task(
                        id=str(uuid.uuid4()),  # Generate new unique ID for the database
                        title=json_task.get('title', ''),
                        description=json_task.get('description', ''),
                        is_completed=json_task.get('completed', False),
                        user_id=user_id
                    )

                    # Handle timestamps if provided in JSON
                    if 'created_at' in json_task:
                        try:
                            task.created_at = datetime.fromisoformat(json_task['created_at'].replace('Z', '+00:00'))
                        except:
                            task.created_at = datetime.utcnow()
                    else:
                        task.created_at = datetime.utcnow()

                    if 'updated_at' in json_task:
                        try:
                            task.updated_at = datetime.fromisoformat(json_task['updated_at'].replace('Z', '+00:00'))
                        except:
                            task.updated_at = datetime.utcnow()
                    else:
                        task.updated_at = datetime.utcnow()

                    session.add(task)
                    session.commit()

                    print(f"Migrated task: {task.title} for user {user_id}")
                    stats["migrated"] += 1

            except Exception as e:
                print(f"Error migrating task {json_task.get('id', 'unknown')}: {e}")
                stats["errors"] += 1

        print(f"Migration completed. Stats: {stats}")
        return stats

    def migrate_users(self, json_file_path: str = "todo_data.json") -> Dict[str, int]:
        """
        Migrate users from JSON file to database based on user references in tasks.

        Args:
            json_file_path: Path to the JSON file containing tasks with user references

        Returns:
            Dictionary with migration statistics
        """
        json_tasks = self.load_json_data(json_file_path)

        if not json_tasks:
            print("No tasks to process for user migration.")
            return {"total_users_processed": 0, "users_created": 0, "users_existing": 0, "errors": 0}

        # Extract unique user_ids from tasks
        user_ids = set()
        for task in json_tasks:
            user_id = task.get('user_id')
            if user_id:
                user_ids.add(user_id)

        stats = {
            "total_users_processed": len(user_ids),
            "users_created": 0,
            "users_existing": 0,
            "errors": 0
        }

        print(f"Processing {len(user_ids)} unique users")

        for user_id in user_ids:
            try:
                with self.SessionLocal() as session:
                    # Check if user already exists
                    user_repo = UserRepository(session)
                    existing_user = user_repo.get_user_by_id_sync(user_id)

                    if existing_user:
                        print(f"User {user_id} already exists.")
                        stats["users_existing"] += 1
                        continue

                    # Create new user
                    email = f"user_{user_id}@example.com"  # Default email if not provided
                    user = User(
                        user_id=user_id,
                        email=email,
                        is_active=True
                    )

                    session.add(user)
                    session.commit()

                    print(f"Created user: {user_id}")
                    stats["users_created"] += 1

            except Exception as e:
                print(f"Error processing user {user_id}: {e}")
                stats["errors"] += 1

        return stats

    def run_full_migration(self, json_file_path: str = "todo_data.json") -> Dict[str, Any]:
        """
        Run full migration: users first, then tasks.

        Args:
            json_file_path: Path to the JSON file containing tasks with user references

        Returns:
            Dictionary with overall migration statistics
        """
        print("Starting full data migration from JSON to database...")

        # Create tables if they don't exist
        SQLModel.metadata.create_all(self.sync_engine)

        # Migrate users first
        user_stats = self.migrate_users(json_file_path)

        # Then migrate tasks
        task_stats = self.migrate_tasks(json_file_path)

        overall_stats = {
            "users": user_stats,
            "tasks": task_stats,
            "summary": {
                "users_processed": user_stats["total_users_processed"],
                "users_created": user_stats["users_created"],
                "tasks_processed": task_stats["total_processed"],
                "tasks_migrated": task_stats["migrated"],
                "tasks_skipped": task_stats["skipped"],
                "total_errors": user_stats["errors"] + task_stats["errors"]
            }
        }

        print("Full migration completed!")
        print(f"Summary: {overall_stats['summary']}")

        return overall_stats


def main():
    """
    Main function to run the migration script.
    """
    import argparse

    parser = argparse.ArgumentParser(description="JSON to Database Migration Tool")
    parser.add_argument("--json-file", type=str, default="todo_data.json",
                       help="Path to the JSON file containing tasks (default: todo_data.json)")
    parser.add_argument("--dry-run", action="store_true",
                       help="Perform a dry run without actually migrating data")
    parser.add_argument("--database-url", type=str,
                       help="Database URL (if not using environment variable)")

    args = parser.parse_args()

    try:
        # Initialize the migration handler
        migrator = JSONToDBMigration(database_url=args.database_url)

        if args.dry_run:
            print("Performing dry run...")
            json_tasks = migrator.load_json_data(args.json_file)
            print(f"Would process {len(json_tasks)} tasks from {args.json_file}")

            # Extract unique user_ids
            user_ids = set()
            for task in json_tasks:
                user_id = task.get('user_id')
                if user_id:
                    user_ids.add(user_id)
            print(f"Would process {len(user_ids)} unique users")
        else:
            # Run the full migration
            result = migrator.run_full_migration(args.json_file)
            print(f"\nMigration completed with result: {result}")

    except Exception as e:
        print(f"Migration failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    # Add sync methods to repositories for migration purposes
    def add_sync_methods():
        """Add synchronous methods to repositories for use in migration."""

        # Add sync method to UserRepository
        def get_user_by_id_sync(self, user_id: str):
            from sqlalchemy import select
            statement = select(User).where(User.user_id == user_id)
            result = self.session.execute(statement)
            return result.scalar_one_or_none()

        UserRepository.get_user_by_id_sync = get_user_by_id_sync

    add_sync_methods()
    exit(main())