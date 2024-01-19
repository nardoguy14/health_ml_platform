
from domain.models import TrainingModel
from torch.nn import Sequential

from repositories.training_models_repository import TrainingModelsRepository

training_models_repository = TrainingModelsRepository()


class TrainingModelsService():

    async def create_training_model(self, training_model: TrainingModel) -> Sequential:
        await training_models_repository.create_training_model(training_model)

        return training_model.training_model_to_torch_sequential()
