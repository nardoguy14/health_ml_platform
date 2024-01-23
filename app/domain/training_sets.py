from pydantic import BaseModel
from typing import Optional
from fastapi import File


class TrainingSet(BaseModel):
    id: Optional[str] = None
    file_name: str
    s3_location: str