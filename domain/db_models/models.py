from sqlalchemy.orm import (DeclarativeBase,
                            Mapped, mapped_column)
from sqlalchemy import String, JSON, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class TrainingModelDB(Base):
    __tablename__ = "training_models"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    training_data_location: Mapped[str] = mapped_column(String(30))
    layers: Mapped[dict] = mapped_column(JSON)
