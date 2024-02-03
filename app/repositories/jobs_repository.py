from app.domain.db_models.jobs import TrainingJobsDB
from app.domain.jobs import TrainingJob
from app.repositories.base_repository import create_db_session


class JobsRepository():

    async def create_job(self, model_id: int, data_set_id: int, job_id: str) -> TrainingJobsDB:
        with create_db_session() as session:
            training_model_db = TrainingJobsDB(
                                       data_set_id=model_id,
                                       model_id=data_set_id,
                                       job_id=job_id)
            session.add(training_model_db)
            session.commit()
            return training_model_db

    async def get_training_job_by_model_id(self, mode_id: int) -> TrainingJobsDB:
        with create_db_session() as session:

            return session.query(TrainingJobsDB).filter(TrainingJobsDB.model_id == mode_id).all()[0]


    async def get_training_job_by_job_id(self, job_id: str) -> TrainingJobsDB:
        with create_db_session() as session:
            return session.query(TrainingJobsDB).filter(TrainingJobsDB.job_id == job_id).all()[0]

    async def update_job_status(self, job_id: str, status: str):
        with create_db_session() as session:
            training_job: TrainingJobsDB = await self.get_training_job_by_job_id(job_id)
            training_job.status = status
            session.merge(training_job)
            session.commit()
            return training_job

