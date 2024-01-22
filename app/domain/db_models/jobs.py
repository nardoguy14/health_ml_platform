from sqlalchemy import String, Integer, DATETIME
from sqlalchemy.orm import (Mapped, mapped_column)
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class TrainingJobsDB(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    data_set_id: Mapped[int] = mapped_column(Integer)
    model_id: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[DATETIME] = mapped_column(DATETIME)
    modified_at: Mapped[DATETIME] = mapped_column(DATETIME)
