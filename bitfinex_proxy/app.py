"""Application description.

Attributes:
    application (BitfinexProxyApplication): Application instance.
"""

import typing as t

from aiohttp import web
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from connections.bitfinex import BitfinexClient
from connections.postgres import (
    init_pg,
    stop_pg,
)
from routes import ROUTES


class BitfinexProxyApplication(web.Application):
    """BitfinexProxy web Application.

    Attributes:
        db_engine (t.Optional[Engine]): Database connection abstraction.
    """

    db_engine: t.Optional[Engine] = None

    def __init__(self, **kwargs):
        """Init application instance."""
        super().__init__(**kwargs)
        self.register_routes()
        self.on_startup.append(init_pg)
        self.on_cleanup.append(stop_pg)
        self.bitfinex_client = BitfinexClient()

    @staticmethod
    def get_db_session() -> Session:
        """Get database session."""
        raise NotImplementedError('Method must be replaced on startup.')

    def register_routes(self):
        """Register all API routes."""
        for route in ROUTES:
            if isinstance(route, web.RouteDef):
                route.register(self.router)
            else:
                self.router.add_view(*route)


application = BitfinexProxyApplication()
