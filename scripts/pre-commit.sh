#!/usr/bin/env bash
set -ex
GIT_ROOT=`git rev-parse --show-toplevel`
cd $GIT_ROOT
flake8 bitfinex_proxy
mypy bitfinex_proxy
pydocstyle bitfinex_proxy
