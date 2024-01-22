from app.domain.db_models.models import TrainingModelDB
from app.domain.models import TrainingModel
from app.repositories.base_repository import create_db_session


class TrainingModelsRepository():

    async def create_training_model(self, training_model: TrainingModel) -> TrainingModel:
        with create_db_session() as session:
            training_model_db = TrainingModelDB(name=training_model.name,
                            training_data_location=training_model.training_data_location,
                            t_dep_column=training_model.t_dep_column,
                            layers=training_model.layers_to_dict())
            session.add(training_model_db)
            session.commit()
            training_model.id = training_model_db.id
            return training_model

    async def get_training_model(self, name: str):
        with create_db_session() as session:
            return session.query(TrainingModelDB).filter(TrainingModelDB.name == name).all()
