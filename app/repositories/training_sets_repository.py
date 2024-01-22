from app.domain.db_models.data_set import DataSetDB
from app.domain.training_sets import TrainingSet
from app.repositories.base_repository import create_db_session


class TrainingSetRepository():

    async def create_training_set(self, training_set: TrainingSet) -> TrainingSet:
        with create_db_session() as session:
            data_set_db = DataSetDB(file_name=training_set.file_name,
                                    s3_location=training_set.s3_location)
            session.add(data_set_db)
            session.commit()
            training_set.id = data_set_db.id
            return training_set

    async def get_training_set(self, file_name: str):
        with create_db_session() as session:
            return session.query(DataSetDB).filter(DataSetDB.file_name == file_name).all()
