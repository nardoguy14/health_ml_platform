import asyncio
import os
import sys

from torch.nn import Sequential
import torch

from app.lib.aws import upload_file_to_s3_file
from app.domain.models import TrainingModel
from app.services.jobs_service import JobsService, TrainingModelsService, TrainingSetsService

jobs_service = JobsService()
training_sets_service = TrainingSetsService()
training_models_service = TrainingModelsService()
JOB_ID = os.environ.get('AWS_BATCH_JOB_ID')


async def run_job(model_name: str, data_set_name: str):
    await jobs_service.update_job_status(JOB_ID, status="STARTING")
    print(f"params model_name: {model_name} data_set_name: {data_set_name}")
    print("getting model")
    training_model: TrainingModel = await training_models_service.get_training_model(model_name)
    print(dict(training_model))
    print("getting training set")
    data_set_file = await training_sets_service.get_training_set(data_set_name)
    print(data_set_file)
    print("running job")
    await jobs_service.update_job_status(JOB_ID, status="TRAINING MODEL")
    trained_model: Sequential = await jobs_service.run_training_job(training_model, data_set_file)
    trained_model_file_name = f"{JOB_ID}_trained_model.pt"
    trained_model_file_path = f'./{trained_model_file_name}'
    torch.save(trained_model.state_dict(), trained_model_file_path)
    await jobs_service.update_job_status(JOB_ID, status="UPLOADING TRAINED MODEL")
    upload_file_to_s3_file(trained_model_file_path, trained_model_file_name)
    await jobs_service.update_job_status(JOB_ID, status="DONE")


model_name = sys.argv[1]
data_set_name = sys.argv[2]

asyncio.run(run_job(model_name, data_set_name))