from fastapi import APIRouter

from app.domain.models import TrainingModel
from app.services.training_models_service import TrainingModelsService

model_router = APIRouter()

training_model_service = TrainingModelsService()


@model_router.post("/training-models/")
async def create_model(training_model: TrainingModel):
    await training_model_service.create_training_model(training_model)
    return 1


@model_router.get("/training-models/{name}")
async def get_model(name: str):
    result = await training_model_service.get_training_model(name)
    return result
