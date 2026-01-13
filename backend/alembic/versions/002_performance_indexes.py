"""Add performance indexes for efficient query performance

Revision ID: 002
Revises: 001
Create Date: 2026-01-13 03:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '002'
down_revision: Union[str, None] = '001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create composite index for common query pattern: user_id + completion status
    op.create_index('idx_tasks_user_id_completed', 'tasks', ['user_id', 'is_completed'])

    # Create index on updated_at for tracking recent changes
    op.create_index('idx_tasks_updated_at', 'tasks', ['updated_at'])

    # Create index on title for potential search functionality (though not currently used)
    op.create_index('idx_tasks_title', 'tasks', ['title'], postgresql_ops={'title': 'varchar_pattern_ops'})

    # Create index on users is_active for filtering active users
    op.create_index('idx_users_is_active', 'users', ['is_active'])


def downgrade() -> None:
    # Drop the performance indexes
    op.drop_index('idx_tasks_title', table_name='tasks')
    op.drop_index('idx_tasks_updated_at', table_name='tasks')
    op.drop_index('idx_tasks_user_id_completed', table_name='tasks')
    op.drop_index('idx_users_is_active', table_name='users')