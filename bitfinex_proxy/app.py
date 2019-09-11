"""Summary.

Attributes:
    application (TYPE): Description.
"""
from aiohttp import web

from routes import ROUTES


class BitfinexProxyApplication(web.Application):
    """BitfinexProxy web Application."""

    def __init__(self, **kwargs):
        """Summary.

        Args:
            **kwargs: Description.
        """
        super().__init__(**kwargs)
        self.register_routes()

    def register_routes(self):
        """Summary."""
        for route in ROUTES:
            if isinstance(route, web.RouteDef):
                route.register(self.router)
            else:
                self.router.add_route(*route)


application = BitfinexProxyApplication()
