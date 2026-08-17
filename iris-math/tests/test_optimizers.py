from optimizers import SGD, Momentum, Adam


parameter = 1.0
gradient = 0.5


sgd = SGD(learning_rate=0.1)
momentum = Momentum(learning_rate=0.1)
adam = Adam(learning_rate=0.1)


print("Initial parameter:", parameter)

print(
    "SGD:",
    sgd.update(parameter, gradient)
)

print(
    "Momentum:",
    momentum.update(parameter, gradient)
)

print(
    "Adam:",
    adam.update(parameter, gradient)
)