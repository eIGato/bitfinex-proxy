"""Postgres connection initialization."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import settings


async def init_pg(app):
    """Initialize PostgreSQL engine."""
    engine = create_engine(settings.POSTGRES_DSN)
    app.db_engine = engine
    app.get_db_session = sessionmaker(bind=engine)


async def stop_pg(app):
    """Stop PostgreSQL engine."""
    app.db_engine.close()
    await app.db_engine.wait_closed()
