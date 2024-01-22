from tempfile import NamedTemporaryFile

import boto3
import tempfile
from fastapi import UploadFile
import os

S3_BUCKET_TRAINING_SETS = os.environ.get("S3_BUCKET_TRAINING_SETS")


def upload_to_s3(upload_file: UploadFile) -> str:
    s3_client = boto3.client('s3')
    with NamedTemporaryFile(mode='w+', delete=False) as temp:
        try:
            contents = upload_file.file.read().decode('utf-8')
            temp.write(contents)
            temp.seek(0)
            result = s3_client.upload_file(temp.name, S3_BUCKET_TRAINING_SETS, upload_file.filename)
            print(result)
            return f"s3://{S3_BUCKET_TRAINING_SETS}/{temp.name}"
        except Exception as e:
            print(e)


def download_from_s3(filename: str):
    s3_client = boto3.client('s3')
    temp_file = NamedTemporaryFile(delete=False)
    result = s3_client.download_fileobj(S3_BUCKET_TRAINING_SETS, filename, temp_file)
    return temp_file

