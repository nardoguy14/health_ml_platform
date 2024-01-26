#!/bin/bash
set -xe


cd /mnt

aws s3 cp s3://nardosml3stack-webappdeploymentbucket-eskd5jc3wx9k/app.zip .

unzip app.zip

mv app/ml.service /etc/systemd/system/ml.service

sudo systemctl daemon-reload

python3 -m venv .venv
. .venv/bin/activate
cd app
pip install -r requirements.txt
