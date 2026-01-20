import asyncio
from logging.config import fileConfig
import os
import sys
import dotenv

# Load environment variables from .env file
dotenv.load_dotenv()

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config
from sqlmodel import SQLModel
from alembic import context
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

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
    # Clean URL for asyncpg (remove unsupported params like sslmode)
    parsed = urlparse(database_url)
    query_params = parse_qs(parsed.query, keep_blank_values=True)
    problematic_params = ['channel_binding', 'sslmode', 'sslcert', 'sslkey', 'sslrootcert']
    
    for param in problematic_params:
        if param in query_params:
            del query_params[param]
            
    # Reconstruct query
    new_query = urlencode(query_params, doseq=True)
    parsed = parsed._replace(query=new_query)
    database_url = urlunparse(parsed)

    # Ensure async driver
    if database_url.startswith("postgresql://"):
        database_url = database_url.replace("postgresql://", "postgresql+asyncpg://", 1)
    elif database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql+asyncpg://", 1)
    config.set_main_option("sqlalchemy.url", database_url)

# Add backend to python path to import models
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import models to populate SQLModel.metadata
# This assumes the new structure in backend/api/database/models/
try:
    from api.database.models import *
except ImportError:
    pass

target_metadata = SQLModel.metadata

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
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
