
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
        await training_models_repository.create_training_model(training_model)

        return training_model.training_model_to_torch_sequential()

    async def get_training_model(self, name: str) -> TrainingModel:
        instance = (await training_models_repository.get_training_model(name))[0]
        layers = []
        for layer in instance.layers:
            layers.append(TrainingLayer(**layer))
        return TrainingModel(name=instance.name,
                             training_data_location=instance.training_data_location,
                             layers=layers)

    async def run_training_model(self, data_loader: DataLoader, data_set: TensorDataset,
                                 training_model: TrainingModel):

        torch_sequential_model = training_model.training_model_to_torch_sequential()
        loss_func = torch.nn.BCELoss()
        optimizer = torch.optim.SGD(torch_sequential_model.parameters(), lr=1e-1, momentum=0.9)
        for epoch in range(40):

            for id_batch, (x_batch, y_batch) in enumerate(data_loader):
                y_batch_pred = torch_sequential_model(x_batch)
                loss = loss_func(y_batch_pred, torch.unsqueeze(y_batch, 1))
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()


            loss = loss.item()
            print(f"epoch: {epoch+1} loss: {loss:>8f}")

        return torch_sequential_model


    async def create_tensors(self, t_dep_col: str, file_name: str):
        data_set = await training_sets_service.get_training_set(file_name)
        df = pandas.read_csv(data_set.name)
        t_dep = torch.tensor(df[t_dep_col])
        t_dep = t_dep.to(torch.float32)

        indep_cols = df.columns.tolist()
        indep_cols.remove(t_dep_col)
        t_indep = torch.tensor(df[indep_cols].values, dtype=torch.float32)
        #get max values along each column
        vals,indices = t_indep.max(dim=0)
        t_indep = t_indep / vals

        return (t_dep, t_indep)

    async def create_data_set_and_data_loaders(self, t_dep, t_indep) -> (TensorDataset, DataLoader):
        trn_indep, val_indep, trn_dep, val_dep = train_test_split(t_indep, t_dep, test_size=0.2, random_state=42)
        dataset = TensorDataset(t_indep, t_dep)
        dataloader = DataLoader(dataset, batch_size=10000, shuffle=True)
        return (dataset, dataloader)

    async def run_training_job(self, model_name: str, data_set_name: str):
        training_model = await self.get_training_model(model_name)
        data_set_file = await training_sets_service.get_training_set(data_set_name)
        t_dep, t_indep = await self.create_tensors(training_model.t_dep_column, data_set_file.name)
        data_set, data_loader = await self.create_data_set_and_data_loaders(t_dep, t_indep)
        trained_model = await self.run_training_model(data_loader, data_set, training_model)
        return trained_model