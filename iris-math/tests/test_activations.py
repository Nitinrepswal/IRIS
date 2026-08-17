from activations import relu, sigmoid, tanh, softmax


values = [-2, 0, 2]

print("ReLU:", [relu(x) for x in values])
print("Sigmoid:", [sigmoid(x) for x in values])
print("Tanh:", [tanh(x) for x in values])

scores = [2.0, 1.0, 0.1]

print("Softmax:", softmax(scores))