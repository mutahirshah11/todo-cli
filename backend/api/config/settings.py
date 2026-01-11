"""
Base API configuration settings for the Todo API.
"""
import os
from typing import List


class Settings:
    """
    Application settings loaded from environment variables.
    Using a simple class instead of Pydantic Settings to avoid field mapping issues.
    """
    def __init__(self):
        # JWT Configuration
        self.jwt_secret_key = os.getenv("JWT_SECRET_KEY", "your-super-secret-key-change-in-production")
        self.jwt_algorithm = os.getenv("JWT_ALGORITHM", "HS256")
        self.access_token_expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

        # Storage Configuration
        self.todo_storage_file = os.getenv("TODO_STORAGE_FILE", "todo_data.json")

        # CORS Configuration
        self.allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "*")

        # Rate Limiting
        self.rate_limit = os.getenv("RATE_LIMIT", "1000/hour")  # 1000 requests per hour per user

        # Logging
        self.log_level = os.getenv("LOG_LEVEL", "INFO")

        # Performance
        self.max_response_time_ms = 100  # Target response time in milliseconds

    def get_allowed_origins(self) -> List[str]:
        """Parse allowed_origins from environment variable."""
        if not self.allowed_origins_env or self.allowed_origins_env.strip() == "":
            return ["*"]
        return [origin.strip() for origin in self.allowed_origins_env.split(",")]


# Create a single instance of settings
settings = Settings()