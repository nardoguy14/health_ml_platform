#!/bin/bash
set -xe


cd /mnt

aws s3 cp s3://nardos5ml-webappdeploymentbucket-wbqxmn6nyeyu/app.zip .

unzip app.zip
rm app.zip
mv app/ml.service /etc/systemd/system/ml.service
sudo chmod 777 /etc/systemd/system/ml.service


python3.9 -m venv .venv
. .venv/bin/activate

pip install -r app/requirements.txt
