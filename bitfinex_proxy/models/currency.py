"""Home for `Currency` model."""
import sqlalchemy as sa

from .base import Base


class Currency(Base):  # type: ignore
    """Model for currency.

    Attributes:
        slug (str): Technical name.
    """

    __tablename__ = 'currency'
    slug: str = sa.Column(sa.String(3), primary_key=True)
