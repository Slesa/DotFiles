#!/bin/sh

# Checks if a commit is reachable by remote branches.

# If any of the following fails, the script fails.
set -e

commitish=`git rev-parse $1`
commitish_short=`git rev-parse --short $1`

on_remote_branches=`git branch --contains=$commitish --remotes`

if [ -n "$on_remote_branches" ]
then
  branch_count=`echo "$on_remote_branches" | wc --lines`

  branch_es=branches
  if [ $branch_count -eq 1 ]
  then
    branch_es=branch
  fi

  echo "$1 ($commitish_short) is reachable by $branch_count remote $branch_es:"
  echo "$on_remote_branches"
else
  echo "$1 ($commitish_short) is not reachable by any remote branch"
fi
