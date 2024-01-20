from pydantic import BaseModel
from typing import Optional
from fastapi import File


class TrainingSet(BaseModel):
    id: Optional[str]
    name: str
    file: File
    location: str
    stored_in_s3: bool = False