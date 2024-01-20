from fastapi import UploadFile, APIRouter
from app.services.training_sets_service import TrainingSetsService

router = APIRouter()
training_sets_service = TrainingSetsService()

@router.post("/training-set/")
async def create_training_set(file: UploadFile):
    await training_sets_service.create_training_set(file)
    return {"filename": file.filename}
