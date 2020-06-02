#!/usr/bin/env bash
set -ex
cat /dev/stdin | pipenv run autopep8 -aa --experimental - | pipenv run isort -
