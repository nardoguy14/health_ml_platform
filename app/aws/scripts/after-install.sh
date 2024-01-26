#!/bin/bash
set -xe


# Copy war file from S3 bucket to tomcat webapp folder
cd /usr/local/app

unzip app.zip

mv ml.service /etc/systemd/system/ml.service

sudo systemctl daemon-reload

python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
