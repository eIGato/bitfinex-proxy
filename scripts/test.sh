#!/usr/bin/env bash
set -ex
CODE=0
WORKDIR=`dirname $0`
cd $WORKDIR/..
PYTHONPATH=./bitfinex_proxy pipenv run pytest $*
