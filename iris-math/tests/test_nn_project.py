import torch
import torch.nn as nn


# ==================================================
# 1. Dataset
# ==================================================

# Features:
# [house_size, bedrooms]

X = torch.tensor([
    [1.0, 1.0],
    [2.0, 1.0],
    [3.0, 2.0],
    [4.0, 2.0],
    [5.0, 3.0],
    [6.0, 3.0],
    [7.0, 4.0],
    [8.0, 4.0]
])

# Target:
# synthetic house price

y = torch.tensor([
    [2.0],
    [3.0],
    [5.0],
    [6.0],
    [8.0],
    [9.0],
    [11.0],
    [12.0]
])


print("Input shape:", X.shape)
print("Target shape:", y.shape)


# ==================================================
# 2. Neural Network
# ==================================================

class HousePriceModel(nn.Module):

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


model = HousePriceModel()


print("\nModel:")
print(model)


# ==================================================
# 3. Loss Function
# ==================================================

loss_function = nn.MSELoss()


# ==================================================
# 4. Optimizer
# ==================================================

optimizer = torch.optim.Adam(
    model.parameters(),
    lr=0.01
)


# ==================================================
# 5. Training
# ==================================================

epochs = 1000

for epoch in range(epochs):

    # Forward propagation
    predictions = model(X)

    # Calculate loss
    loss = loss_function(
        predictions,
        y
    )

    # Clear old gradients
    optimizer.zero_grad()

    # Backpropagation
    loss.backward()

    # Update weights
    optimizer.step()

    if (epoch + 1) % 200 == 0:

        print(
            f"Epoch: {epoch + 1}, "
            f"Loss: {loss.item():.6f}"
        )


# ==================================================
# 6. Final predictions
# ==================================================

with torch.no_grad():

    predictions = model(X)


print("\nFinal predictions:")

print(predictions)


print("\nActual values:")

print(y)


# ==================================================
# 7. Test on unseen houses
# ==================================================

new_houses = torch.tensor([
    [9.0, 5.0],
    [10.0, 5.0]
])

with torch.no_grad():

    new_predictions = model(new_houses)


print("\nNew houses:")

print(new_houses)


print("\nPredicted prices:")

print(new_predictions)