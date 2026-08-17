import torch


x = torch.tensor([2.0, 3.0])

w = torch.tensor([0.5, 0.8])

b = torch.tensor(0.2)

z = torch.sum(x * w) + b

print("Inputs:", x)
print("Weights:", w)
print("Bias:", b)
print("Weighted sum:", z)