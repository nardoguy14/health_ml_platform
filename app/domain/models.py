from pydantic import BaseModel
from typing import Optional
from fastapi import File
from torch.nn import Module, Linear, Sequential, ReLU, Sigmoid

class TrainingLayer(BaseModel):
    training_type: str
    in_layers: int
    out_layers: int


class TrainingModel(BaseModel):
    id: Optional[int] = None
    name: str
    training_data_location: str
    t_dep_column: str
    layers: list[TrainingLayer]

    def training_model_to_torch_sequential(self) -> Sequential:
        torch_layers = []
        for layer in self.layers:
            if layer.training_type == "Linear":
                torch_layers.append(Linear(layer.in_layers, layer.out_layers))
                torch_layers.append(ReLU())
        del torch_layers[len(torch_layers)-1]
        torch_layers.append(Sigmoid())
        model = Sequential(*torch_layers)
        return model

    def layers_to_dict(self):
        result = []
        for layer in self.layers:
            result.append(dict(layer))
        return result