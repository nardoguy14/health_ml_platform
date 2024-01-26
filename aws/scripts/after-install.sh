#!/bin/bash
set -xe


cd /usr/local/app

aws s3 cp s3://nardoml3stack-webappdeploymentbucket-9zouy4hd1xrr/app.zip .

unzip app.zip

mv app/ml.service /etc/systemd/system/ml.service

sudo systemctl daemon-reload

python3 -m venv .venv
. .venv/bin/activate
cd app
pip install -r requirements.txt
