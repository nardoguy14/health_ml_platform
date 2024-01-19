from domain.db_models.models import TrainingModelDB
from domain.models import TrainingModel
from repositories.base_repository import create_db_session


class TrainingModelsRepository():

    async def create_training_model(self, training_model: TrainingModel):
        with create_db_session() as session:
            training_model_db = TrainingModelDB(name=training_model.name,
                            training_data_location=training_model.training_data_location,
                            layers=training_model.layers_to_dict())
            session.add(training_model_db)
            session.commit()


