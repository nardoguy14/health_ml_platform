from app.domain.db_models.jobs import TrainingJobsDB
from app.domain.jobs import TrainingJob
from app.repositories.base_repository import create_db_session


class JobsRepository():

    async def create_job(self, model_id: int, data_set_id: int) -> TrainingJobsDB:
        with create_db_session() as session:
            training_model_db = TrainingJobsDB(name="",
                                       data_set_id=model_id,
                                       model_id=data_set_id)
            session.add(training_model_db)
            session.commit()
            return training_model_db

    async def get_training_job(self, name: str):
        with create_db_session() as session:
            return session.query(TrainingJobsDB).filter(TrainingJobsDB.name == name).all()
