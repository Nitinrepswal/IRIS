import torch
import torch.nn as nn


# -------------------------
# Dataset
# -------------------------

x = torch.tensor([
    [1.0],
    [2.0],
    [3.0],
    [4.0],
    [5.0],
    [6.0],
    [7.0],
    [8.0],
    [9.0],
    [10.0]
])

y = torch.tensor([
    [2.0],
    [4.0],
    [6.0],
    [8.0],
    [10.0],
    [12.0],
    [14.0],
    [16.0],
    [18.0],
    [20.0]
])


# -------------------------
# Split
# -------------------------

x_train = x[:6]
y_train = y[:6]

x_validation = x[6:8]
y_validation = y[6:8]

x_test = x[8:]
y_test = y[8:]


# -------------------------
# Model
# -------------------------

model = nn.Linear(1, 1)

loss_function = nn.MSELoss()

optimizer = torch.optim.SGD(
    model.parameters(),
    lr=0.01
)


# -------------------------
# Training
# -------------------------

for epoch in range(1000):

    predictions = model(x_train)

    loss = loss_function(predictions, y_train)

    optimizer.zero_grad()

    loss.backward()

    optimizer.step()


# -------------------------
# Evaluation
# -------------------------

with torch.no_grad():

    train_predictions = model(x_train)
    validation_predictions = model(x_validation)
    test_predictions = model(x_test)

    train_loss = loss_function(
        train_predictions,
        y_train
    )

    validation_loss = loss_function(
        validation_predictions,
        y_validation
    )

    test_loss = loss_function(
        test_predictions,
        y_test
    )


print("Train loss:", train_loss.item())
print("Validation loss:", validation_loss.item())
print("Test loss:", test_loss.item())

print("\nTest predictions:")
print(test_predictions)