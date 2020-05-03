#!/bin/sh
update-rc.d xvfb defaults
#Xvfb :99 -screen 0 2560x1600x24 &
Xvnc :99
xvfb-run --server-num=99 --server-args="-screen 0 2560x1600x24" python3 ./scripts/script.py 2>&1