"""Home for `Rate` model."""
from datetime import date
from decimal import Decimal
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from .base import Base


class Rate(Base):  # type: ignore
    """Model for currency rate.

    Attributes:
        id (UUID): PK.
        currency_slug (str): Currency foreign key.
        traded_at (date): Date of trading.
        rate (Decimal): Selected currency to USD rate.
        volume (Decimal): Daily trading volume.
    """

    __tablename__ = 'rate'
    id: UUID = sa.Column(postgresql.UUID(as_uuid=True), primary_key=True)
    currency_slug: str = sa.Column(
        sa.String(3),
        sa.ForeignKey('currency.slug'),
    )
    traded_at: date = sa.Column(sa.Date)
    rate: Decimal = sa.Column(sa.Numeric(precision=5))
    volume: Decimal = sa.Column(sa.Numeric(precision=5))