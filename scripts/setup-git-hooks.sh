#!/usr/bin/env bash
set -ex
GIT_ROOT=`git rev-parse --show-toplevel`
HOOK_NAMES="
    pre-commit
    pre-push
"
for HOOK_NAME in $HOOK_NAMES; do
    rm -f $GIT_ROOT/.git/hooks/$HOOK_NAME
    ln -s $GIT_ROOT/scripts/$HOOK_NAME.sh $GIT_ROOT/.git/hooks/$HOOK_NAME
done
git config filter.autostyle.clean scripts/autostyle.sh
git config filter.autostyle.smudge cat
