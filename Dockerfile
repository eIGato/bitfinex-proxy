FROM python:3.6

COPY requirements.txt /tmp/

RUN mkdir -p /tmp/bitfinex_proxy/.pytest_cache/ && \
    pip install -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt

COPY src/ setup.cfg scripts/test.sh /app/

ENV PYTHONPATH="./bitfinex_proxy"

WORKDIR /app/
