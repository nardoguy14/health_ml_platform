import tempfile
from fastapi import APIRouter

from app.domain.jobs import TrainingJob
from app.services.jobs_service import JobsService
from fastapi import UploadFile, APIRouter, File
import shutil

job_router = APIRouter()

jobs_service = JobsService()


@job_router.post("/training-job/")
async def create_job(training_model: TrainingJob):
    training_job = await jobs_service.create_job(training_model)
    return training_job

@job_router.post("/inference/model/{model_name}")
async def run_inference(model_name: str, file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        shutil.copyfileobj(file.file, temp_file)
        temp_file.seek(0)
        result = await jobs_service.run_inference_job(temp_file, model_name)
        return {
            "result": result
        }
