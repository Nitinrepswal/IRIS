import torch
import torch.nn as nn


class MLP(nn.Module):

    def __init__(self):
        super().__init__()

        self.network = nn.Sequential(
            nn.Linear(2, 8),
            nn.ReLU(),
            nn.Linear(8, 4),
            nn.ReLU(),
            nn.Linear(4, 1)
        )

    def forward(self, x):
        return self.network(x)


model = MLP()

print("Model:")
print(model)


x = torch.tensor([
    [1.0, 2.0],
    [2.0, 3.0],
    [3.0, 4.0]
])


output = model(x)

print("Input:")
print(x)

print("Output:")
print(output)