from fastapi import UploadFile, APIRouter
from fastapi.responses import StreamingResponse

from app.services.training_sets_service import TrainingSetsService

router = APIRouter()
training_sets_service = TrainingSetsService()

@router.post("/training-set/")
async def create_training_set(file: UploadFile):
    await training_sets_service.create_training_set(file)
    return {"filename": file.filename}


@router.get("/training-set/{file_name}")
async def get_training_set(file_name: str):
    file = await training_sets_service.get_training_set(file_name)
    file.seek(0)

    return StreamingResponse(iter([file.read()]), media_type="text/plain",
                             headers={"Content-Disposition": f"attachment; filename={file_name}"})

