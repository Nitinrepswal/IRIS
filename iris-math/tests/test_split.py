import torch


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


# Split the data
x_train = x[:6]
y_train = y[:6]

x_validation = x[6:8]
y_validation = y[6:8]

x_test = x[8:]
y_test = y[8:]


print("Training data:")
print(x_train)
print(y_train)

print("\nValidation data:")
print(x_validation)
print(y_validation)

print("\nTest data:")
print(x_test)
print(y_test)