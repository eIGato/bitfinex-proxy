"""Home for `Currency` model."""
from sqlalchemy import (
    Column,
    String,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base: type = declarative_base()


class Currency(Base):  # type: ignore
    """Model for currency.

    Attributes:
        id (UUID): PK.
        slug (str): Technical name.
    """

    __tablename__ = 'currency'

    id = Column(UUID(as_uuid=True), primary_key=True)
    slug = Column(String(3))
