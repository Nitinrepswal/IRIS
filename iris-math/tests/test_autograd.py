import torch


weight = torch.tensor(
    0.2,
    requires_grad=True
)

x = torch.tensor(2.0)

target = torch.tensor(1.0)


prediction = weight * x

loss = (prediction - target) ** 2


print("Weight:", weight)
print("Prediction:", prediction)
print("Loss:", loss)


loss.backward()


print("Weight gradient:", weight.grad)