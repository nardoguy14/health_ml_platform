from sqlalchemy import String, Integer, DATETIME
from sqlalchemy.orm import (Mapped, mapped_column)
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class DataSetDB(Base):
    __tablename__ = "data_set"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    s3_location: Mapped[str] = mapped_column(String(130))
    file_name: Mapped[str] = mapped_column(String(30))
    created_at: Mapped[DATETIME] = mapped_column(DATETIME)
    modified_at: Mapped[DATETIME] = mapped_column(DATETIME)
