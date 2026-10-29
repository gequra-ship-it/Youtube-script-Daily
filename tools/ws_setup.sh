#!/bin/bash
# usage: ws_setup.sh <ws-dir> <slug>   -> sandbox copy of the repo parts needed to rebuild a few scenes and run tools/motionaudit.py
set -e; WS=$1; S=$2; R=/home/user/youtube-script-daily
mkdir -p $WS/videos $WS/render $WS/work
cp -r $R/tools $WS/tools; cp -r $R/docs $WS/docs 2>/dev/null || true
cp -r $R/videos/$S $WS/videos/$S; cp -r $R/render/$S $WS/render/$S
cp -r /tmp/miya-work/$S $WS/work/$S
echo "ws ready: cd $WS && MIYA_WORK=$WS/work SLUG=$S SEL=<scene numbers> python3 tools/build3.py   (VERT=1 for shorts)"
