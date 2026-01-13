# Neon Database Backup Configuration
# This file contains configuration for automated backup procedures

BACKUP_SCHEDULE = {
    "enabled": True,
    "frequency": "daily",  # Options: hourly, daily, weekly
    "time": "02:00",       # Time in HH:MM format (UTC)
    "retention_days": 30,  # How many days to keep backups
    "backup_directory": "./backups",
    "compress": True       # Whether to compress backup files
}

# Point-in-time recovery settings
PITR_SETTINGS = {
    "enabled": True,       # Neon handles PITR internally, this is for reference
    "rpo_target_seconds": 60,  # Recovery Point Objective (max data loss)
    "rto_target_minutes": 5    # Recovery Time Objective (max downtime)
}

# Backup notification settings
NOTIFICATION_SETTINGS = {
    "email_on_success": False,
    "email_on_failure": True,
    "admin_emails": ["admin@example.com"]
}

# Backup validation settings
VALIDATION_SETTINGS = {
    "validate_after_creation": True,
    "validation_timeout_seconds": 300,
    "required_tables": ["users", "tasks"]
}

# Remote storage settings (for production)
REMOTE_STORAGE = {
    "enabled": False,      # Enable for production deployments
    "provider": "aws_s3",  # Options: aws_s3, gcp_storage, azure_blob
    "bucket_name": "my-backup-bucket",
    "region": "us-east-1"
}