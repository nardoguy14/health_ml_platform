#!/bin/bash
set -xe

# Delete the old  directory as needed.
if [ -d /mnt/ ]; then
    cd /mnt
    rm -rf *
fi

