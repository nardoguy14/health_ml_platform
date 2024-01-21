from tempfile import NamedTemporaryFile

import boto3
import tempfile
from fastapi import UploadFile
import os

S3_BUCKET_TRAINING_SETS = os.environ.get("S3_BUCKET_TRAINING_SETS")


def upload_to_s3(upload_file: UploadFile):
    s3_client = boto3.client('s3')
    with NamedTemporaryFile(delete=False) as temp:
        try:
            contents = upload_file.file.read()
            temp.write(contents)
            result = s3_client.upload_file(temp.name, S3_BUCKET_TRAINING_SETS, 'myfile.txt')
        except Exception as e:
            print(e)


def download_from_s3(filename: str):
    s3_client = boto3.client('s3')
    temp_file = tempfile.NamedTemporaryFile()
    s3_client.download_file(S3_BUCKET_TRAINING_SETS, filename, temp_file.name)
    return temp_file

