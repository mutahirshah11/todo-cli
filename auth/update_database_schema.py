#!/usr/bin/env python3
"""
Script to update the auth_users table schema to add the name column
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import ProgrammingError

# Load environment variables from .env file
load_dotenv()

def update_auth_users_table():
    # Get database URL from environment
    database_url = os.getenv("NEON_DATABASE_URL")
    if not database_url:
        print("Error: NEON_DATABASE_URL environment variable not set")
        return False

    print(f"Connecting to database...")

    # Create engine and connect
    engine = create_engine(database_url)

    try:
        with engine.connect() as conn:
            # Check if the name column exists
            check_column_query = """
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = 'auth_users' AND column_name = 'name'
            """

            result = conn.execute(text(check_column_query))
            column_exists = result.fetchone() is not None

            if column_exists:
                print("Name column already exists in auth_users table")
                return True
            else:
                print("Adding name column to auth_users table...")

                # Add the name column with a default value
                alter_query = "ALTER TABLE auth_users ADD COLUMN name VARCHAR(255) DEFAULT '' NOT NULL"
                conn.execute(text(alter_query))
                conn.commit()

                print("Successfully added name column to auth_users table")
                return True

    except ProgrammingError as e:
        if 'does not exist' in str(e) and 'auth_users' in str(e):
            print("Error: auth_users table doesn't exist yet. You need to start the auth service once to create the initial schema.")
            return False
        else:
            print(f"Error modifying database: {e}")
            return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("Updating auth_users table schema...")
    success = update_auth_users_table()
    if success:
        print("Schema update completed successfully!")
    else:
        print("Schema update failed!")