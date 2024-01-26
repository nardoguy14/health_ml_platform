#!/bin/bash
set -xe

# Start Tomcat, the application server.
cd /mnt

. .venv/bin/activate

gunicorn -b 0.0.0.0:8000 -p uvicorn.pid -k uvicorn.workers.UvicornWorker app.main:app
