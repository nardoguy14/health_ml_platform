#!/bin/bash
set -xe


cd /usr/local/app

aws s3 cp s3://nardomlstack-webappdeploymentbucket-00batakrvsbh/app.zip .

unzip app.zip

mv app/ml.service /etc/systemd/system/ml.service

sudo systemctl daemon-reload

python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
