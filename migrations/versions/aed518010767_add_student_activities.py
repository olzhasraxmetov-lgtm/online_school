"""add student activities

Revision ID: aed518010767
Revises: acdb4bf3a2da
Create Date: 2026-10-03 13:32:08.519650

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = 'aed518010767'
down_revision: Union[str, Sequence[str], None] = 'acdb4bf3a2da'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('student_activities',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('student_id', sa.String(length=36), nullable=False),
    sa.Column('course_id', sa.String(length=36), nullable=False),
    sa.Column('activity_type', sa.String(length=50), nullable=False),
    sa.Column('entity_id', sa.String(length=36), nullable=False),
    sa.Column('title', sa.Text(), nullable=False),
    sa.Column('details', sa.JSON(), nullable=False),
    sa.Column('occurred_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['student_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_student_activities_activity_type'), 'student_activities', ['activity_type'], unique=False)
    op.create_index(op.f('ix_student_activities_course_id'), 'student_activities', ['course_id'], unique=False)
    op.create_index(op.f('ix_student_activities_occurred_at'), 'student_activities', ['occurred_at'], unique=False)
    op.create_index(op.f('ix_student_activities_student_id'), 'student_activities', ['student_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_student_activities_student_id'), table_name='student_activities')
    op.drop_index(op.f('ix_student_activities_occurred_at'), table_name='student_activities')
    op.drop_index(op.f('ix_student_activities_course_id'), table_name='student_activities')
    op.drop_index(op.f('ix_student_activities_activity_type'), table_name='student_activities')
    op.drop_table('student_activities')
