import math

def relu(x):
    return max(0, x)

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def tanh(x):
    return math.tanh(x)

def softmax(values):
    exponentials = []

    for value in values:
        exponentials.append(math.exp(value))

    total = sum(exponentials)

    probabilities = []

    for value in exponentials:
        probabilities.append(value / total)

    return probabilities