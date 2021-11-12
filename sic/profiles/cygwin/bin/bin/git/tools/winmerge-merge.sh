#!/bin/sh
#
# export GIT_DIFFMERGE_VERBOSE=1 to enable logging
#

script_path=${0%/*}
source "$script_path/diff-and-merge-support.sh"

mergetool="/c/Tools/WinMerge/WinMergeU.exe"
get_merge_args "$1" "$2" "$3" "$4"

"$mergetool" /e /u /wl /dl "Mine" /dr "Theirs" "$local" "$remote" "$result"
