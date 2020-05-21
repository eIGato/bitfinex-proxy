FROM python:3.8-slim

RUN mkdir -p /app/ && \
    pip install pipenv

COPY bitfinex_proxy/ Pipfile Pipfile.lock setup.cfg scripts/test.sh /app/

WORKDIR /app/

RUN mkdir -p /tmp/bitfinex_proxy/.pytest_cache/ && \
    pipenv install --system --ignore-pipfile --clear --deploy --dev

ENV PYTHONPATH="."

CMD ["gunicorn", "app:application", "-k", "aiohttp.GunicornUVLoopWebWorker"]
