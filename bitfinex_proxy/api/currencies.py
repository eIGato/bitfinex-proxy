"""Home for `/currencies/` API branch."""

import typing as t
from datetime import (
    date,
    timedelta,
)
from decimal import Decimal
from itertools import chain

import ujson as json
from aiohttp import web
from sqlalchemy.orm import Session

from models import (
    Currency,
    Rate,
)
from settings import VOLUME_AGG_SPAN


def get_volume_avg(rates: t.Iterable[Rate]) -> Decimal:
    """Calculate average trade volume for given rates."""
    return sum(rate.volume for rate in rates) / Decimal(VOLUME_AGG_SPAN)


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

    async def get(self) -> web.Response:
        """Get currency with rate and trading volume."""
        slug = self.request.match_info['slug'].upper()
        if not 2 <= len(slug) <= 3:
            return web.Response(text='', status=400)
        today = date.today()
        session: Session = self.request.app.get_db_session()  # type: ignore
        currency = session.query(Currency).filter(
            Currency.slug == slug,
        ).one_or_none()
        bitfinex_client = self.request.app.bitfinex_client  # type: ignore
        if currency is not None:
            rates = session.query(Rate).filter(
                Rate.currency_slug == slug,
                Rate.traded_at >= today - timedelta(VOLUME_AGG_SPAN),
            )
            rates_count = rates.count()
            if rates_count >= VOLUME_AGG_SPAN:
                return web.Response(
                    text=json.dumps({
                        'slug': slug,
                        'last_rate': rates[-1].rate,
                        'volume_avg': get_volume_avg(rates),
                    }),
                    content_type='application/json',
                )
            fresh_rates = await bitfinex_client.get_rates(
                slug,
                VOLUME_AGG_SPAN - rates_count,
                today=today,
            )
            for rate in fresh_rates:
                session.add(rate)
            session.commit()
            return web.Response(
                text=json.dumps({
                    'slug': slug,
                    'last_rate': fresh_rates[-1].rate,
                    'volume_avg': get_volume_avg(chain(rates, fresh_rates)),
                }),
                content_type='application/json',
            )
        fresh_rates = await bitfinex_client.get_rates(
            slug,
            VOLUME_AGG_SPAN,
            today=today,
        )
        if not fresh_rates:
            return web.Response(text='', status=400)
        currency = Currency(slug=slug)
        session.add(currency)
        for rate in fresh_rates:
            session.add(rate)
        session.commit()
        return web.Response(
            text=json.dumps({
                'slug': slug,
                'last_rate': fresh_rates[-1].rate,
                'volume_avg': get_volume_avg(fresh_rates),
            }),
            content_type='application/json',
        )
