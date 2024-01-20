from fastapi import UploadFile
import os

from app.lib.aws import upload_to_s3
from app.lib.file_helpers import store_file_locally


class TrainingSetsService():

    async def create_training_set(self, file: UploadFile):
        if os.environ.get("STORE_IN_S3", False):
            upload_to_s3(file)
        else:
            await store_file_locally(file)
