"""Home for `/currencies/` API branch."""

import json
from datetime import (
    date,
    timedelta,
)

from aiohttp import web
from sqlalchemy.orm import Session

from models import (
    Currency,
    Rate,
)
from settings import VOLUME_AGG_SPAN


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


class CurrencyView(web.View):
    """View currency by slug."""

    async def get(self, slug: str) -> web.Response:
        """Get currency with rate and trading volume."""
        if not 2 <= len(slug) <= 3:
            return web.Response(status=404)
        today = date.today()
        slug = slug.upper()
        session: Session = self.request.app.get_db_session()  # type: ignore
        currency = session.query(Currency).filter(
            Currency.slug == slug,
        ).one_or_none()
        bitfinex_client = self.request.app.bitfinex_client  # type: ignore
        if currency is not None:
            rates = session.query(currency.rates).filter(
                Rate.traded_at >= today - timedelta(VOLUME_AGG_SPAN),
            )
            if len(rates) >= VOLUME_AGG_SPAN:
                return web.Response(
                    text=json.dumps({
                        'slug': slug,
                        'rates': [dict(rate) for rate in rates],
                    }),
                    content_type='application/json',
                )
            fresh_rates = await bitfinex_client.get_rates(
                slug,
                VOLUME_AGG_SPAN - len(rates),
                today=today,
            )
            session.add(fresh_rates)
            session.commit()
            return web.Response(
                text=json.dumps({
                    'slug': slug,
                    'rates': [dict(rate) for rate in rates + fresh_rates],
                }),
                content_type='application/json',
            )
        fresh_rates = await bitfinex_client.get_rates(
            slug,
            VOLUME_AGG_SPAN,
            today=today,
        )
        if not fresh_rates:
            return web.Response(status=404)
        currency = Currency(slug=slug)
        session.add(currency)
        session.add(fresh_rates)
        session.commit()
        return web.Response(
            text=json.dumps({
                'slug': slug,
                'rates': [dict(rate) for rate in fresh_rates],
            }),
            content_type='application/json',
        )
