"""API routes description."""
import typing as t

from aiohttp import web

from api import currencies

ROUTES: t.Tuple[t.Union[web.RouteDef, t.Tuple[str, t.Type[web.View]]], ...] = (
    ('/api/currencies/', currencies.CurrencyListView),
    ('/api/currencies/{slug}', currencies.CurrencyView),
)
