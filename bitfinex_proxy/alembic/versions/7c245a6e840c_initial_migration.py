"""Initial migration.

Revision ID: 7c245a6e840c
Revises:
Create Date: 2020-05-28 15:27:55.048074
"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = '7c245a6e840c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """Migrate forward."""
    op.create_table(
        'currency',
        sa.Column('slug', sa.String(length=3), nullable=False),
        sa.PrimaryKeyConstraint('slug'),
    )
    op.create_table(
        'rate',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('currency_slug', sa.String(length=3), nullable=False),
        sa.Column('traded_at', sa.Date(), nullable=False),
        sa.Column('rate', sa.Numeric(precision=5), nullable=False),
        sa.Column('volume', sa.Numeric(precision=5), nullable=False),
        sa.ForeignKeyConstraint(['currency_slug'], ['currency.slug']),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade():
    """Migrate backward."""
    op.drop_table('rate')
    op.drop_table('currency')
