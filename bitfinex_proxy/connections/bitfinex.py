"""Connection to Bitfinex."""

import typing as t
from datetime import (
    date,
    datetime,
    timedelta,
)

import aiohttp

from models import Rate
from settings import DEFAULT_CURRENCY_SLUG


def get_milliseconds(date_: date) -> int:
    """Convert date to millisecond timestamp."""
    return int(datetime(*(
        date_.timetuple()[:-3]  # type: ignore
    )).timestamp()) * 1000


class BitfinexClient:
    """Client to Bitfinex API."""

    BITFINEX_URL = 'https://api-pub.bitfinex.com/v2/'
    CANDLES_ENDPOINT_TEMPLATE = (
        BITFINEX_URL
        + 'candles/trade:1D:t{currency_slug}'
        + DEFAULT_CURRENCY_SLUG
        + '/hist?start={start}&end={end}&sort=1'
    )

    def __init__(self):
        """Init client instance."""
        self.session = aiohttp.ClientSession()

    def __del__(self):
        """Clean up client instance."""
        self.session._loop.run_until_complete(self.session.close())

    async def get_rates(
        self,
        currency_slug: str,
        days: int,
        today: date,
    ) -> t.List[Rate]:
        """Get trade info about given currency for a few last days."""
        if currency_slug == DEFAULT_CURRENCY_SLUG:
            return []
        start_date = today - timedelta(days)
        response = await self.session.get(
            self.CANDLES_ENDPOINT_TEMPLATE.format(
                currency_slug=currency_slug,
                start=get_milliseconds(start_date),
                end=get_milliseconds(today),
            ),
        )
        candles = await response.json()
        return [
            Rate.from_candle(
                candle,
                traded_at=start_date + timedelta(day),
                currency_slug=currency_slug,
            )
            for day, candle in enumerate(candles)
        ]
