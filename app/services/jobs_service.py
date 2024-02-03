from tempfile import NamedTemporaryFile

import pandas
import torch
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, TensorDataset
from torch.nn import Sequential
import numpy

from app.lib.aws import create_batch_job, download_from_s3
from app.domain.db_models.jobs import TrainingJobsDB
from app.domain.jobs import TrainingJob
from app.domain.models import TrainingModel
from app.repositories.jobs_repository import JobsRepository
from app.services.training_models_service import TrainingModelsService
from app.services.training_sets_service import TrainingSetsService

jobs_repository = JobsRepository()
training_sets_service = TrainingSetsService()
training_models_service = TrainingModelsService()


class JobsService():

    async def create_job(self, training_job: TrainingJob):
        training_model: TrainingModel = await training_models_service.get_training_model(training_job.model_name)
        data_set_meta: TrainingJobsDB = await training_sets_service.get_training_set_meta(training_job.data_set_name)
        job_id = create_batch_job(training_job.model_name, training_job.data_set_name)
        job = await jobs_repository.create_job(training_model.id, data_set_meta.id, job_id)
        return job

    async def update_job_status(self, job_id: str, status: str):
        await jobs_repository.update_job_status(job_id, status)

    async def run_training_job(self, training_model: TrainingModel, data_set_file: NamedTemporaryFile):
        t_dep, t_indep = await self.create_tensors(training_model.t_dep_column, data_set_file)
        data_set, data_loader = await self.create_data_set_and_data_loaders(t_dep, t_indep)
        trained_model = await self.run_training_model(data_loader, data_set, training_model)
        return trained_model

    async def run_inference_job(self, test_set_file: NamedTemporaryFile, model_name: str):
        tensors = await self.create_indep_tensors(test_set_file)
        dataset = TensorDataset(tensors)
        dataloader = DataLoader(dataset, batch_size=5000)
        model = await training_models_service.get_training_model(model_name)
        torch_model = model.training_model_to_torch_sequential()
        trained_model_file: NamedTemporaryFile = download_from_s3(f"{model.name}_trained_model.pt")
        trained_model_state_dict = torch.load(trained_model_file.name)
        torch_model.load_state_dict(trained_model_state_dict)
        torch_model.eval()
        with torch.no_grad():
            results = []
            for x in dataloader:
                scores = torch_model(x[0])
                results.append(scores.numpy().tolist())

            return results


    async def get_job_from_model_id(self, model_id):
        return await jobs_repository.get_training_job_by_job_id(model_id)

    async def run_training_model(self, data_loader: DataLoader, data_set: TensorDataset,
                                 training_model: TrainingModel) -> Sequential:

        torch_sequential_model: Sequential = training_model.training_model_to_torch_sequential()
        loss_func = torch.nn.BCELoss()
        optimizer = torch.optim.SGD(torch_sequential_model.parameters(), lr=1e-1, momentum=0.9)
        for epoch in range(40):

            for id_batch, (x_batch, y_batch) in enumerate(data_loader):
                y_batch_pred = torch_sequential_model(x_batch)
                loss = loss_func(y_batch_pred, torch.unsqueeze(y_batch, 1))
                optimizer.zero_grad()
                loss.backward()
                optimizer. step()


            loss = loss.item()
            print(f"epoch: {epoch+1} loss: {loss:>8f}")

        return torch_sequential_model


    async def create_tensors(self, t_dep_col: str, data_set_file: NamedTemporaryFile):
        df = pandas.read_csv(data_set_file.name)
        t_dep = torch.tensor(df[t_dep_col])
        t_dep = t_dep.to(torch.float32)

        indep_cols = df.columns.tolist()
        indep_cols.remove(t_dep_col)
        t_indep = torch.tensor(df[indep_cols].values, dtype=torch.float32)
        #get max values along each column
        vals,indices = t_indep.max(dim=0)
        t_indep = t_indep / vals

        return (t_dep, t_indep)

    async def create_indep_tensors(self, data_set_file: NamedTemporaryFile):
        df = pandas.read_csv(data_set_file.name)
        indep_cols = df.columns.tolist()
        t_indep = torch.tensor(df[indep_cols].values, dtype=torch.float32)
        #get max values along each column
        vals,indices = t_indep.max(dim=0)
        t_indep = t_indep / vals
        return t_indep

    async def create_data_set_and_data_loaders(self, t_dep, t_indep) -> (TensorDataset, DataLoader):
        trn_indep, val_indep, trn_dep, val_dep = train_test_split(t_indep, t_dep, test_size=0.2, random_state=42)
        dataset = TensorDataset(t_indep, t_dep)
        dataloader = DataLoader(dataset, batch_size=10000, shuffle=True)
        return (dataset, dataloader)
