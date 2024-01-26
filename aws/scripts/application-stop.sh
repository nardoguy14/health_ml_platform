#!/bin/bash
set -x

if [ -e /etc/systemd/system/ml.service ]; then
    sudo systemctl stop ml
fi