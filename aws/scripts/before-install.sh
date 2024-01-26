#!/bin/bash
set -xe

# Delete the old  directory as needed.
if [ -d /usr/local/app/ ]; then
    rm -rf /usr/local/app/
fi

mkdir -vp /usr/local/app

#aws s3 cp s3://nardomlstack-webappdeploymentbucket-00batakrvsbh/app.zip /usr/local/app

ls

