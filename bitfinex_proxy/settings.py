"""Application settings."""
from os import environ

DEFAULT_CURRENCY_SLUG = 'USD'
DEFAULT_POSTGRES_DSN = 'postgres://postgres:postgres@postgres/bitfinex_proxy'
POSTGRES_DSN = environ.get('POSTGRES_DSN', DEFAULT_POSTGRES_DSN)
VOLUME_AGG_SPAN = 10
