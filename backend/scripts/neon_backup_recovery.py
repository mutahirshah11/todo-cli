"""
Neon Database Backup and Recovery Procedures
This script provides backup and recovery capabilities for Neon PostgreSQL database
"""

import os
import subprocess
import asyncio
import json
from datetime import datetime
from typing import Dict, List, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NeonBackupRecovery:
    """
    Class to handle Neon database backup and recovery operations.
    """

    def __init__(self, database_url: Optional[str] = None):
        """
        Initialize the backup and recovery handler.

        Args:
            database_url: PostgreSQL database URL. If not provided, uses DATABASE_URL environment variable.
        """
        self.database_url = database_url or os.getenv("DATABASE_URL")
        if not self.database_url:
            raise ValueError("DATABASE_URL must be provided either as parameter or environment variable")

        # Parse database URL to extract components
        from urllib.parse import urlparse
        parsed = urlparse(self.database_url)
        self.db_host = parsed.hostname
        self.db_port = parsed.port or 5432
        self.db_name = parsed.path.lstrip('/')
        self.db_user = parsed.username
        self.db_password = parsed.password

    def create_backup(self, backup_dir: str = "./backups", backup_name: Optional[str] = None) -> str:
        """
        Create a backup of the Neon database using pg_dump.

        Args:
            backup_dir: Directory to store the backup file
            backup_name: Custom name for the backup file (without extension)

        Returns:
            Path to the created backup file
        """
        import os
        from pathlib import Path

        # Create backup directory if it doesn't exist
        Path(backup_dir).mkdir(parents=True, exist_ok=True)

        # Generate backup name if not provided
        if not backup_name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"neon_backup_{self.db_name}_{timestamp}"

        backup_file = os.path.join(backup_dir, f"{backup_name}.sql")

        # Set up environment for pg_dump
        env = os.environ.copy()
        env['PGPASSWORD'] = self.db_password

        # Build pg_dump command
        cmd = [
            'pg_dump',
            '-h', self.db_host,
            '-p', str(self.db_port),
            '-U', self.db_user,
            '-d', self.db_name,
            '-f', backup_file,
            '--verbose',
            '--clean',  # Include DROP statements
            '--if-exists',  # Use IF EXISTS with DROP
            '--no-owner',  # Don't include ownership information
            '--no-privileges',  # Don't include access privileges
        ]

        try:
            logger.info(f"Starting database backup to {backup_file}")
            result = subprocess.run(cmd, env=env, capture_output=True, text=True, check=True)
            logger.info(f"Backup completed successfully: {backup_file}")
            logger.debug(f"pg_dump output: {result.stdout}")
            return backup_file
        except subprocess.CalledProcessError as e:
            logger.error(f"Backup failed: {e}")
            logger.error(f"pg_dump error output: {e.stderr}")
            raise
        except FileNotFoundError:
            logger.error("pg_dump command not found. Please ensure PostgreSQL client tools are installed.")
            raise

    def restore_backup(self, backup_file: str) -> bool:
        """
        Restore a database from a backup file using psql.

        Args:
            backup_file: Path to the backup file to restore from

        Returns:
            True if restoration was successful, False otherwise
        """
        if not os.path.exists(backup_file):
            raise FileNotFoundError(f"Backup file does not exist: {backup_file}")

        # Set up environment for psql
        env = os.environ.copy()
        env['PGPASSWORD'] = self.db_password

        # Build psql command
        cmd = [
            'psql',
            '-h', self.db_host,
            '-p', str(self.db_port),
            '-U', self.db_user,
            '-d', self.db_name,
            '-f', backup_file,
            '--echo-all',
            '--set', 'ON_ERROR_STOP=1'
        ]

        try:
            logger.info(f"Starting database restore from {backup_file}")
            result = subprocess.run(cmd, env=env, capture_output=True, text=True, check=True)
            logger.info("Restore completed successfully")
            logger.debug(f"psql output: {result.stdout}")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Restore failed: {e}")
            logger.error(f"psql error output: {e.stderr}")
            raise
        except FileNotFoundError:
            logger.error("psql command not found. Please ensure PostgreSQL client tools are installed.")
            raise

    def point_in_time_recovery(self, target_time: str, backup_file: str) -> bool:
        """
        Perform point-in-time recovery to a specific timestamp.
        Note: This is a simplified version - full PITR requires WAL shipping setup.

        Args:
            target_time: Target timestamp for recovery (ISO format)
            backup_file: Path to the base backup file

        Returns:
            True if recovery was successful, False otherwise
        """
        logger.warning("Point-in-time recovery requires WAL shipping setup which is typically managed by Neon internally.")
        logger.info(f"For Neon, point-in-time recovery is usually handled through the Neon console.")
        logger.info(f"Restoring from base backup: {backup_file}")
        return self.restore_backup(backup_file)

    async def validate_backup_integrity(self, backup_file: str) -> Dict[str, any]:
        """
        Validate the integrity of a backup file by checking its content.

        Args:
            backup_file: Path to the backup file to validate

        Returns:
            Dictionary containing validation results
        """
        validation_result = {
            'valid': False,
            'size': 0,
            'contains_expected_tables': [],
            'errors': []
        }

        try:
            # Get file size
            validation_result['size'] = os.path.getsize(backup_file)

            # Check if file is empty
            if validation_result['size'] == 0:
                validation_result['errors'].append("Backup file is empty")
                return validation_result

            # Look for expected table definitions in the dump
            expected_tables = ['users', 'tasks']
            with open(backup_file, 'r', encoding='utf-8') as f:
                content = f.read(10000)  # Read first 10KB to check for table definitions

                for table in expected_tables:
                    if f'TABLE public.{table}' in content or f'CREATE TABLE {table}' in content:
                        validation_result['contains_expected_tables'].append(table)

            # If we found expected content, consider it valid
            if len(validation_result['contains_expected_tables']) > 0:
                validation_result['valid'] = True
            else:
                validation_result['errors'].append("Expected table definitions not found in backup")

        except Exception as e:
            validation_result['errors'].append(str(e))

        return validation_result

    def get_backup_list(self, backup_dir: str = "./backups") -> List[Dict[str, any]]:
        """
        Get a list of available backups in the specified directory.

        Args:
            backup_dir: Directory to scan for backup files

        Returns:
            List of dictionaries containing backup information
        """
        import os
        from pathlib import Path

        backups = []
        backup_path = Path(backup_dir)

        if not backup_path.exists():
            return backups

        for file_path in backup_path.glob("*.sql"):
            stat = file_path.stat()
            backups.append({
                'filename': file_path.name,
                'size': stat.st_size,
                'created_at': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'full_path': str(file_path.absolute())
            })

        # Sort by creation time (newest first)
        backups.sort(key=lambda x: x['created_at'], reverse=True)
        return backups


def main():
    """
    Main function to demonstrate backup and recovery operations.
    """
    import argparse

    parser = argparse.ArgumentParser(description="Neon Database Backup and Recovery Tool")
    parser.add_argument("--action", choices=["backup", "restore", "validate", "list"], required=True,
                       help="Action to perform: backup, restore, validate, or list")
    parser.add_argument("--backup-file", type=str, help="Path to backup file (required for restore/validate)")
    parser.add_argument("--backup-dir", type=str, default="./backups", help="Directory for backup operations")
    parser.add_argument("--backup-name", type=str, help="Custom name for backup file")

    args = parser.parse_args()

    # Initialize the backup/recovery handler
    try:
        backup_handler = NeonBackupRecovery()
    except ValueError as e:
        logger.error(f"Failed to initialize: {e}")
        return 1

    try:
        if args.action == "backup":
            backup_path = backup_handler.create_backup(
                backup_dir=args.backup_dir,
                backup_name=args.backup_name
            )
            logger.info(f"Backup created: {backup_path}")

        elif args.action == "restore":
            if not args.backup_file:
                logger.error("--backup-file is required for restore action")
                return 1
            success = backup_handler.restore_backup(args.backup_file)
            if success:
                logger.info("Restore completed successfully")
            else:
                logger.error("Restore failed")

        elif args.action == "validate":
            if not args.backup_file:
                logger.error("--backup-file is required for validate action")
                return 1
            validation_result = asyncio.run(backup_handler.validate_backup_integrity(args.backup_file))
            logger.info(f"Validation result: {validation_result}")

        elif args.action == "list":
            backups = backup_handler.get_backup_list(args.backup_dir)
            if backups:
                print("Available backups:")
                for backup in backups:
                    print(f"  {backup['filename']} ({backup['size']} bytes, {backup['created_at']})")
            else:
                print("No backups found in directory")

    except Exception as e:
        logger.error(f"Operation failed: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())