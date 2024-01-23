import os

from fastapi import UploadFile

from app.domain.training_sets import TrainingSet
from app.lib.aws import upload_to_s3, download_from_s3
from app.lib.file_helpers import store_file_locally, get_file_locally
from app.repositories.training_sets_repository import TrainingSetRepository

training_set_repository = TrainingSetRepository()

class TrainingSetsService():

    async def create_training_set(self, file: UploadFile):
        if os.environ.get("STORE_IN_S3", False):
            url = upload_to_s3(file)
            await training_set_repository.create_training_set(TrainingSet(file_name=file.filename, s3_location=url))
        else:
            await store_file_locally(file)

    async def get_training_set(self, file_name: str):
        if os.environ.get("STORE_IN_S3", False):
            return download_from_s3(file_name)
        else:
            return get_file_locally(file_name)

    async def get_training_set_meta(self, file_name: str):
        meta = await training_set_repository.get_training_set(file_name)
        return meta[0]

