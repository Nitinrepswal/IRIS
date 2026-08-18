import torch
import torch.nn as nn


class RepresentationModel(nn.Module):

    def __init__(self):
        super().__init__()

        # Learn a representation
        self.encoder = nn.Sequential(
            nn.Linear(2, 4),
            nn.ReLU()
        )

        # Use the representation for prediction
        self.decoder = nn.Linear(4, 1)

    def forward(self, x):

        representation = self.encoder(x)

        prediction = self.decoder(representation)

        return representation, prediction


# --------------------------------------------------
# Dataset
# --------------------------------------------------

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


# --------------------------------------------------
# Model
# --------------------------------------------------

model = RepresentationModel()

loss_function = nn.MSELoss()

optimizer = torch.optim.Adam(
    model.parameters(),
    lr=0.01
)


# --------------------------------------------------
# Training
# --------------------------------------------------

for epoch in range(1000):

    representation, prediction = model(x)

    loss = loss_function(
        prediction,
        y
    )

    optimizer.zero_grad()

    loss.backward()

    optimizer.step()

    if (epoch + 1) % 200 == 0:

        print(
            f"Epoch: {epoch + 1}, "
            f"Loss: {loss.item():.6f}"
        )


# --------------------------------------------------
# Final representation
# --------------------------------------------------

with torch.no_grad():

    representation, prediction = model(x)


print("\nLearned representation:")
print(representation)

print("\nFinal predictions:")
print(prediction)

print("\nActual values:")
print(y)