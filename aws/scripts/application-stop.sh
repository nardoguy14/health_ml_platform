#!/bin/bash
set -x

if [ -e /mnt/uvicorn.pid ]; then
    pid=$(cat uvicorn.pid)
    kill -9 $pid
fi
