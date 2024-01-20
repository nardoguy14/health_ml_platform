from fastapi import UploadFile, APIRouter

from app.domain.models import TrainingModel
from app.services.training_models_service import TrainingModelsService

model_router = APIRouter()

training_model_service = TrainingModelsService()

@model_router.post("/training-models/")
async def create_model(training_model: TrainingModel):
    await training_model_service.create_training_model(training_model)
    return 1
