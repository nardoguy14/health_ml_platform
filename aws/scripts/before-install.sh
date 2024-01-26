#!/bin/bash
set -xe

# Delete the old  directory as needed.
if [ -d /usr/local/app/ ]; then
    rm -rf /usr/local/app/
fi

mkdir -vp /usr/local/app

ls

