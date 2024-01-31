#!/bin/bash
set -xe


cd /mnt

aws s3 cp s3://nardosmlplatform-webappdeploymentbucket-cadt7kio1hej/app.zip .

unzip app.zip
rm app.zip
mv tmp/* .


python3.9 -m venv .venv
. .venv/bin/activate

pip install -r app/requirements.txt

. /etc/environment

cd app

alembic upgrade head

