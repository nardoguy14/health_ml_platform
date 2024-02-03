import tempfile
from fastapi import APIRouter
import numpy

from app.domain.jobs import TrainingJob
from app.services.jobs_service import JobsService
from fastapi import UploadFile, APIRouter, File
import shutil

job_router = APIRouter()

jobs_service = JobsService()


@job_router.post("/job/training/")
async def create_job(training_model: TrainingJob):
    training_job = await jobs_service.create_job(training_model)
    return training_job

@job_router.post("/job/inference/model/{model_name}")
async def run_inference_job(model_name: str, file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        shutil.copyfileobj(file.file, temp_file)
        temp_file.seek(0)
        result = await jobs_service.run_inference_job(temp_file, model_name)
        flattened = collape_results(result)
        positive_cases, percent = calculate_stats(flattened)

        return {
            "raw_results": flattened,
            "stats": {
                "positive_cases": positive_cases,
                "percent": percent
            }
        }


def collape_results(result: list):
    flattened = []
    for par in result:
        for item in par:
            flattened.append(item[0])
    return flattened


def calculate_stats(items)-> (float,float):
    cutoff = 0.5
    positive_cases = 0
    for item in items:
        if item > cutoff:
            positive_cases += 1
    percent = positive_cases/len(items)
    return positive_cases, percent
