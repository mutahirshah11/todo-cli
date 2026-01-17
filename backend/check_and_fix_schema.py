#!/usr/bin/env python3
"""
Script to check and fix the database schema by adding the missing 'name' column to the users table.
"""

import os
import dotenv
from sqlalchemy import create_engine, text

# Load environment variables
dotenv.load_dotenv()

def check_and_fix_schema():
    # Get database URL from environment
    database_url = os.getenv("NEON_DATABASE_URL")
    if not database_url:
        print("Error: NEON_DATABASE_URL environment variable not set")
        return False

    print("Connecting to database...")

    # Create sync engine (using psycopg2)
    engine = create_engine(database_url)

    try:
        with engine.connect() as conn:
            # Check if the name column exists in the users table
            result = conn.execute(text("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = 'users' AND column_name = 'name'
            """))

            column_exists = result.fetchone() is not None

            if column_exists:
                print("[OK] Name column already exists in users table")
                return True
            else:
                print("[MISSING] Name column does not exist in users table. Adding it...")

                # Add the name column to the users table
                conn.execute(text("ALTER TABLE users ADD COLUMN name VARCHAR(255) DEFAULT '' NOT NULL"))
                conn.commit()

                print("[SUCCESS] Successfully added name column to users table")
                return True

    except Exception as e:
        print(f"[ERROR] Error modifying database: {e}")
        return False

if __name__ == "__main__":
    print("Checking and fixing database schema...")

    success = check_and_fix_schema()

    if success:
        print("\n[SUCCESS] Schema check and fix completed successfully!")
    else:
        print("\n[FAILED] Schema check and fix failed!")