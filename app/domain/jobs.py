from typing import Optional

from pydantic import BaseModel
from app.domain.models import TrainingModel


class TrainingJob(BaseModel):
    id: Optional[int] = None
    model_name: str
    data_set_name: str
    job_id: Optional[str] = None