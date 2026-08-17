import torch


# Training data
x = torch.tensor([[1.0], [2.0], [3.0], [4.0]])
y = torch.tensor([[2.0], [4.0], [6.0], [8.0]])


# Simple model
model = torch.nn.Linear(1, 1)


# Loss function
loss_function = torch.nn.MSELoss()


# Optimizer
optimizer = torch.optim.SGD(
    model.parameters(),
    lr=0.01
)


# Training loop
for epoch in range(1000):

    # Forward pass
    predictions = model(x)

    # Calculate loss
    loss = loss_function(predictions, y)

    # Clear old gradients
    optimizer.zero_grad()

    # Backpropagation
    loss.backward()

    # Update parameters
    optimizer.step()


print("Final predictions:")
print(model(x))

print("Final loss:", loss.item())

print("Weight:", model.weight.item())
print("Bias:", model.bias.item())