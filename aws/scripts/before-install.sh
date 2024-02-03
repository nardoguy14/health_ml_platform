#!/bin/bash
set -xe

# Delete the old  directory as needed.
if [ -d /mnt/ ]; then
    cd /mnt

    if [ -d "alembic" ]; then
      rm -rf alembic
    fi

    if [ -d "app" ]; then
      rm -rf app
    fi

    if [ -d "alembic.ini" ]; then
      rm alembic.ini
    fi
fi

