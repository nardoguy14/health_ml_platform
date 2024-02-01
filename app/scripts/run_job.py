import asyncio
import sys

from app.domain.models import TrainingModel
from app.services.jobs_service import JobsService, TrainingModelsService, TrainingSetsService

jobs_service = JobsService()
training_sets_service = TrainingSetsService()
training_models_service = TrainingModelsService()


async def run_job(model_name: str, data_set_name: str):
    print(f"params model_name: {model_name} data_set_name: {data_set_name}")
    print("getting model")
    training_model: TrainingModel = await training_models_service.get_training_model(model_name)
    print(dict(training_model))
    print("getting training set")
    data_set_file = await training_sets_service.get_training_set(data_set_name)
    print(data_set_file)
    print("running job")
    trained_model = await jobs_service.run_training_job(training_model, data_set_file)


model_name = sys.argv[1]
data_set_name = sys.argv[2]

asyncio.run(run_job(model_name, data_set_name))