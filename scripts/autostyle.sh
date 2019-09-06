#!/usr/bin/env bash
set -ex
cat /dev/stdin | autopep8 -aa --experimental - | isort -
