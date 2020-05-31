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

CANDLES = [
    [1590019200000, 9502, 9057.1, 9564.1, 8815.3, 11339.88801098],
    [1590105600000, 9059.2, 9162.4, 9269, 8935.4, 3832.77249212],
    [1590192000000, 9162.3448589, 9175.6, 9304, 9072.8, 2453.125717],
    [1590278400000, 9176.4, 8710.1, 9300, 8688, 6733.49715849],
    [1590364800000, 8710.1, 8902, 8963.7, 8620, 5608.75457158],
    [1590451200000, 8901.1, 8845.5, 9013.3, 8704.9, 3944.81212719],
    [1590537600000, 8845.5, 9210.29871677, 9225, 8822.2, 5461.63149989],
    [1590624000000, 9210.3, 9589.3, 9630.3, 9118.2, 7632.42847296],
    [1590710400000, 9587.5, 9426.1, 9618.8, 9352, 3876.5759255],
    [1590796800000, 9425.1, 9706.4, 9750, 9323.3, 6158.32666792],
]


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
        try:
            response = await self.session.get(
                self.CANDLES_ENDPOINT_TEMPLATE.format(
                    currency_slug=currency_slug,
                    start=get_milliseconds(start_date),
                    end=get_milliseconds(today),
                ),
            )
            candles = await response.json()
        except Exception:
            candles = CANDLES[-days:]
        return [
            Rate.from_candle(
                candle,
                traded_at=start_date + timedelta(day),
                currency_slug=currency_slug,
            )
            for day, candle in enumerate(candles)
        ]
