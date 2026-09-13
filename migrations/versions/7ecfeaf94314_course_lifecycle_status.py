"""course lifecycle status

Revision ID: 7ecfeaf94314
Revises: 41d877562106
Create Date: 2026-09-13 15:48:58.214151

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = '7ecfeaf94314'
down_revision: Union[str, Sequence[str], None] = '41d877562106'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('courses', sa.Column('status', sa.String(length=32), nullable=False, server_default='draft'))
    op.create_index(op.f('ix_courses_status'), 'courses', ['status'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_courses_status'), table_name='courses')
    op.drop_column('courses', 'status')
