"""Application settings."""
from os import environ

DEFAULT_POSTGRES_DSN = 'postgres://postgres:postgres@postgres/bitfinex_proxy'
POSTGRES_DSN = environ.get('POSTGRES_DSN', DEFAULT_POSTGRES_DSN)
