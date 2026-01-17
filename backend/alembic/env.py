from logging.config import fileConfig
import os
import sys
import dotenv

# Load environment variables from .env file
dotenv.load_dotenv()

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Read database URL from environment variable
database_url = os.getenv("NEON_DATABASE_URL")
if database_url:
    config.set_main_option("sqlalchemy.url", database_url)

# add your model's MetaData object here
# for 'autogenerate' support
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api.models.database import User, Task
target_metadata = User.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    if not url:
        # Provide a dummy URL for autogenerate when not connected to actual database
        url = "postgresql://user:pass@localhost/dbname"

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=False,  # Changed to False to avoid error during autogenerate
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # Read database URL from environment variable
    database_url = os.getenv("NEON_DATABASE_URL")
    if database_url:
        config.set_main_option("sqlalchemy.url", database_url)

    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

    with context.begin_transaction():
        context.run_migrations()


# Check if this is being run for autogenerate by checking command options
# Alembic provides access to command options through config.cmd_opts
if context.is_offline_mode():
    run_migrations_offline()
elif hasattr(context.config, 'cmd_opts') and getattr(context.config.cmd_opts, 'autogenerate', False):
    # When autogenerate is specified, run offline to avoid needing a real database connection
    run_migrations_offline()
else:
    run_migrations_online()