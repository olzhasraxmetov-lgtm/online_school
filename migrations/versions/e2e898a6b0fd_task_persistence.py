"""task persistence

Revision ID: e2e898a6b0fd
Revises: a55a05c81b36
Create Date: 2026-08-30 15:47:00.004791

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = 'e2e898a6b0fd'
down_revision: Union[str, Sequence[str], None] = 'a55a05c81b36'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('tasks',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('section_id', sa.String(length=36), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('statement', sa.Text(), nullable=False),
    sa.Column('position', sa.Integer(), nullable=False),
    sa.Column('check_type', sa.String(length=50), nullable=False),
    sa.Column('expected_answer', sa.Text(), nullable=False),
    sa.Column('accepted_answers', sa.JSON(), nullable=False),
    sa.Column('answer_pattern', sa.Text(), nullable=False),
    sa.Column('max_attempts', sa.Integer(), nullable=False),
    sa.Column('reward_points', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['section_id'], ['sections.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('task_attempts',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('task_id', sa.String(length=36), nullable=False),
    sa.Column('student_id', sa.String(length=36), nullable=False),
    sa.Column('submitted_answer', sa.Text(), nullable=False),
    sa.Column('attempt_number', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=50), nullable=False),
    sa.Column('awarded_points', sa.Integer(), nullable=True),
    sa.Column('checked_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['student_id'], ['users.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('progress', sa.Column('completed_task_ids', sa.JSON(), nullable=False, server_default='[]'))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('progress', 'completed_task_ids')
    op.drop_table('task_attempts')
    op.drop_table('tasks')
