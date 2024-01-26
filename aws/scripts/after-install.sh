#!/bin/bash
set -xe


cd /mnt

aws s3 cp s3://nardoml4stack-webappdeploymentbucket-zaboqhj73weq/app.zip .

unzip app.zip

mv app/ml.service /etc/systemd/system/ml.service

sudo systemctl daemon-reload

python3 -m venv .venv
. .venv/bin/activate
cd app
pip install -r requirements.txt
