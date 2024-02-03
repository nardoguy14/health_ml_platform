#!/bin/bash
set -x

if [ -e "/mnt/uvicorn.pid" ]; then
    pid=$(cat /mnt/uvicorn.pid)
    sudo kill -9 $pid
    sudo rm /mnt/uvicorn.pid
fi
