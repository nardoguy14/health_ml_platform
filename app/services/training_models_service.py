
import pandas
import torch
from sklearn.model_selection import train_test_split
from torch.nn import Sequential
from torch.utils.data import DataLoader, TensorDataset

from app.domain.models import TrainingModel, TrainingLayer
from app.repositories.training_models_repository import TrainingModelsRepository
from app.services.training_sets_service import TrainingSetsService

training_models_repository = TrainingModelsRepository()
training_sets_service = TrainingSetsService()


class TrainingModelsService():

    async def create_training_model(self, training_model: TrainingModel) -> Sequential:
        result = await training_models_repository.create_training_model(training_model)

        return result

    async def get_training_model(self, name: str) -> TrainingModel:
        instance = (await training_models_repository.get_training_model(name))[0]
        layers = []
        for layer in instance.layers:
            layers.append(TrainingLayer(**layer))
        return TrainingModel(id=instance.id,
                             name=instance.name,
                             training_data_location=instance.training_data_location,
                             layers=layers)
