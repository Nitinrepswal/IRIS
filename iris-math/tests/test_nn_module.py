import torch
import torch.nn as nn


class SimpleModel(nn.Module):
    def __init__(self):
        super().__init__()

        self.linear = nn.Linear(1, 1)

    def forward(self, x):
        return self.linear(x)


model = SimpleModel()

print("Model:")
print(model)

print("Weight:", model.linear.weight)
print("Bias:", model.linear.bias)

x = torch.tensor([[1.0], [2.0], [3.0]])

output = model(x)

print("Input:", x)
print("Output:", output)