"""Fix decimal fields.

Revision ID: aaea441b24f4
Revises: 7c245a6e840c
Create Date: 2020-06-01 17:23:45.075983
"""
import sqlalchemy as sa
from alembic import op

revision = 'aaea441b24f4'
down_revision = '7c245a6e840c'
branch_labels = None
depends_on = None


def upgrade():
    """Migrate forward."""
    op.alter_column(
        'rate',
        'rate',
        type_=sa.Numeric(precision=16, scale=8),
    )
    op.alter_column(
        'rate',
        'volume',
        type_=sa.Numeric(precision=16, scale=8),
    )


def downgrade():
    """Migrate backward."""
    op.alter_column(
        'rate',
        'rate',
        type_=sa.Numeric(precision=5),
    )
    op.alter_column(
        'rate',
        'volume',
        type_=sa.Numeric(precision=5),
    )
