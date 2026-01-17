#!/usr/bin/env python3
"""
Script to verify the name column exists in the auth_users table
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load environment variables from .env file
load_dotenv()

def verify_name_column():
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
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_name = 'auth_users' AND column_name = 'name'
            """

            result = conn.execute(text(check_column_query))
            row = result.fetchone()

            if row:
                column_name, data_type, is_nullable = row
                print(f"Name column exists in auth_users table")
                print(f"   Column name: {column_name}")
                print(f"   Data type: {data_type}")
                print(f"   Is nullable: {is_nullable}")
                return True
            else:
                print("Name column does not exist in auth_users table")
                return False

    except Exception as e:
        print(f"Error verifying database: {e}")
        return False

if __name__ == "__main__":
    print("Verifying auth_users table schema...")
    success = verify_name_column()
    if success:
        print("Verification completed successfully!")
    else:
        print("Verification failed!")