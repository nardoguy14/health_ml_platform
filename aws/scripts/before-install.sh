#!/bin/bash
set -xe

# Delete the old  directory as needed.
if [ -d /mnt/data/ ]; then
    rm -rf /mnt/data/app/
fi

