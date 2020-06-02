#!/usr/bin/env bash
set -ex
GIT_ROOT=`git rev-parse --show-toplevel`
cd $GIT_ROOT
scripts/test.sh -m smoke >> /dev/null
