#!/bin/sh
xvfb-run --server-num=99 --server-args="-screen 0 2560x1600x24" python3 /src/scripts/script.py 2>&1