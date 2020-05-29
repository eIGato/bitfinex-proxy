"""Home for `/currencies/` API branch."""

import json

from aiohttp import web
from sqlalchemy.orm import Session

from models import Currency


class CurrencyListView(web.View):
    """List all currency slugs."""

    async def get(self) -> web.Response:
        """Get currency list."""
        session: Session = self.request.app.get_db_session()  # type: ignore
        currencies = session.query(Currency).all()
        return web.Response(
            text=json.dumps([currency.slug for currency in currencies]),
            content_type='application/json',
        )
