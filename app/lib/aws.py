from tempfile import NamedTemporaryFile

import boto3
import json

import tempfile
from fastapi import UploadFile
import os

from app.lib.utils import generate_random_string

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
            return f"s3://{S3_BUCKET_TRAINING_SETS}/{upload_file.filename}"
        except Exception as e:
            print(e)


def download_from_s3(filename: str) -> NamedTemporaryFile:
    s3_client = boto3.client('s3')
    temp_file = NamedTemporaryFile(delete=False)
    result = s3_client.download_fileobj(S3_BUCKET_TRAINING_SETS, filename, temp_file)
    temp_file.seek(0)
    return temp_file


def create_batch_job(model_name: str, data_set_name: str) -> str:
    batch_client = boto3.client('batch')
    r = generate_random_string(5)
    job_name = f'ml_batch_job_{r}'
    job_queue = 'arn:aws:batch:us-east-1:132856321237:job-queue/ml_job_queue_main'
    job_definition = 'arn:aws:batch:us-east-1:132856321237:job-definition/ml_job_definition:5'
    command_overrides = [model_name, data_set_name]
    container_overrides = {
        'command': command_overrides
    }
    response = batch_client.submit_job(
        jobName=job_name,
        jobQueue=job_queue,
        jobDefinition=job_definition,
        shareIdentifier=generate_random_string(),
        containerOverrides=container_overrides,
    )

    job_id = response['jobId']
    print(response)
    print(job_id)
    return job_id


def get_job_details(job_id: str) -> dict:
    c = boto3.client('batch')
    result = c.describe_jobs(jobs=[job_id])
    pretty_json = json.dumps(result, indent=2)
    print(pretty_json)
    return result




