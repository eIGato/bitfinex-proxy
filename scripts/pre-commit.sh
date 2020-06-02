#!/usr/bin/env bash
set -ex
GIT_ROOT=`git rev-parse --show-toplevel`
cd $GIT_ROOT
pipenv run flake8 bitfinex_proxy
pipenv run mypy bitfinex_proxy
pipenv run pydocstyle bitfinex_proxy
