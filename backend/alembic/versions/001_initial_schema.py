"""Initial database schema with User and Task tables

Revision ID: 001
Revises:
Create Date: 2026-01-13 02:50:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
import sqlmodel
import uuid


# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create users table
    op.create_table('users',
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.PrimaryKeyConstraint('user_id'),
        sa.UniqueConstraint('email')
    )

    # Create index for email
    op.create_index('idx_users_email', 'users', ['email'])

    # Create tasks table
    op.create_table('tasks',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_completed', sa.Boolean(), nullable=False, default=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes for tasks
    op.create_index('idx_tasks_user_id', 'tasks', ['user_id'])
    op.create_index('idx_tasks_completed', 'tasks', ['is_completed'])
    op.create_index('idx_tasks_created_at', 'tasks', ['created_at'])


def downgrade() -> None:
    # Drop indexes first
    op.drop_index('idx_tasks_created_at', table_name='tasks')
    op.drop_index('idx_tasks_completed', table_name='tasks')
    op.drop_index('idx_tasks_user_id', table_name='tasks')
    op.drop_index('idx_users_email', table_name='users')

    # Drop tables
    op.drop_table('tasks')
    op.drop_table('users')