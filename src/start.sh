#!/bin/sh
echo '-> Your container args are:' "$@"
if [ "$#" -eq 4 ]; then
  xvfb-run --server-num=99 --server-args="-screen 0 2560x1600x24" python3 ./cli.py "$1" "$2" "$3" "$4" 2>&1
elif [ "$#" -eq 2 ]; then
  xvfb-run --server-num=99 --server-args="-screen 0 2560x1600x24" python3 ./cli.py "$1" "$2" 2>&1
fi