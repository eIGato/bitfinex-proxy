"""Home for `Currency` model."""
import sqlalchemy as sa
from sqlalchemy.orm import relationship

from .base import Base


class Currency(Base):  # type: ignore
    """Model for currency.

    Attributes:
        slug (str): Technical name.
    """

    __tablename__ = 'currency'

    slug: str = sa.Column(sa.String(3), primary_key=True)

    rates = relationship(
        'Rate',
        order_by='Rate.traded_at',
        back_populates='currency',
        cascade='all, delete, delete-orphan',
    )
