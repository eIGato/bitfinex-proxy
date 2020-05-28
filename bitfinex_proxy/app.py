"""Application description.

Attributes:
    application (BitfinexProxyApplication): Application instance.
"""
from aiohttp import web

from routes import ROUTES


class BitfinexProxyApplication(web.Application):
    """BitfinexProxy web Application."""

    def __init__(self, **kwargs):
        """Init application instance."""
        super().__init__(**kwargs)
        self.register_routes()

    def register_routes(self):
        """Register all API routes."""
        for route in ROUTES:
            if isinstance(route, web.RouteDef):
                route.register(self.router)
            else:
                self.router.add_route(*route)


application = BitfinexProxyApplication()
