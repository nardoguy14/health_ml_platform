from fastapi import APIRouter

from app.domain.jobs import TrainingJob
from app.services.jobs_service import JobsService

job_router = APIRouter()

jobs_service = JobsService()


@job_router.post("/training-job/")
async def create_job(training_model: TrainingJob):
    training_job = await jobs_service.create_job(training_model)
    return training_job
