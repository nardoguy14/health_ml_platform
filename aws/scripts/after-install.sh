#!/bin/bash
set -xe


cd /mnt

aws s3 cp s3://nardosfinalml-webappdeploymentbucket-5dtphqts3nhh/app.zip .

unzip app.zip
rm app.zip


python3.9 -m venv .venv
. .venv/bin/activate

pip install -r app/requirements.txt

. /etc/environment

cd app

alembic upgrade head

