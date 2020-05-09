#!/bin/sh
echo '-> Your container args are:' "$@"
xvfb-run --server-num=99 --server-args="-screen 0 2560x1600x24" python3 ./script.py "$1" "$2" 2>&1