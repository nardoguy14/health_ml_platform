#!/bin/bash
set -xe

# Start Tomcat, the application server.
cd /mnt

. .venv/bin/activate
sudo chmod 777 /mnt

. /etc/environment
export STORE_IN_S3=1

gunicorn -b 0.0.0.0:8080 -p uvicorn.pid -k uvicorn.workers.UvicornWorker app.main:app --daemon --error-logfile logs.txt --capture-output
