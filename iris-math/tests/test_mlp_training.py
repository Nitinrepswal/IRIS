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


# Dataset
x = torch.tensor([
    [1.0, 2.0],
    [2.0, 3.0],
    [3.0, 4.0],
    [4.0, 5.0]
])

y = torch.tensor([
    [3.0],
    [5.0],
    [7.0],
    [9.0]
])


# Model
model = MLP()


# Loss
loss_function = nn.MSELoss()


# Optimizer
optimizer = torch.optim.Adam(
    model.parameters(),
    lr=0.01
)


# Training
for epoch in range(1000):

    predictions = model(x)

    loss = loss_function(predictions, y)

    optimizer.zero_grad()

    loss.backward()

    optimizer.step()

    if (epoch + 1) % 100 == 0:
        print(
            f"Epoch: {epoch + 1}, "
            f"Loss: {loss.item():.6f}"
        )


# Final predictions
print("\nFinal predictions:")
print(model(x))

print("\nFinal loss:")
print(loss.item())