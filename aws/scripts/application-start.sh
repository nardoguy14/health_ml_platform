#!/bin/bash
set -xe

# Start Tomcat, the application server.
cd /mnt

. .venv/bin/activate

uvicorn app.main:app
