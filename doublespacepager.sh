#!/bin/bash

# Produces a double-spaced, pager-ed view of a file. Can be piped to or called
# with an argument representing a file.

[ $# -eq 1 -a -f "$1" ] && input="$1" || input=" -"
cat $input | pr -d -t | less
