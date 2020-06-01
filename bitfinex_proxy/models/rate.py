"""Home for `Rate` model."""
import typing as t
from datetime import date
from decimal import Decimal
from uuid import (
    UUID,
    uuid4,
)

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship

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

    id: UUID = sa.Column(
        postgresql.UUID(as_uuid=True),
        default=uuid4,
        primary_key=True,
    )
    currency_slug: str = sa.Column(
        sa.String(3),
        sa.ForeignKey('currency.slug'),
        nullable=False,
    )
    traded_at: date = sa.Column(sa.Date, nullable=False)
    rate: Decimal = sa.Column(
        sa.Numeric(precision=16, scale=8),
        nullable=False,
    )
    volume: Decimal = sa.Column(
        sa.Numeric(precision=16, scale=8),
        nullable=False,
    )

    currency = relationship('Currency', back_populates='rates')

    @classmethod
    def from_candle(
        cls,
        candle: t.List[float],
        traded_at: date,
        currency_slug: str,
    ) -> 'Rate':
        """Build `Rate` instance from Bitfinex candle."""
        return cls(
            currency_slug=currency_slug,
            traded_at=traded_at,
            rate=candle[2],
            volume=candle[5],
        )

    def to_dict(self) -> dict:
        """Convert `Rate` instance to `dict`."""
        return {
            attr: getattr(self, attr)
            for attr in [
                'currency_slug',
                'rate',
                'volume',
            ]
        }
