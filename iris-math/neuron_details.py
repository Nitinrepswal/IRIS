class Neuron:
    def __init__(self, weights, bias):
        self.weights = weights
        self.bias = bias

    def weighted_sum(self, inputs):
        total = 0.0

        for i in range(len(inputs)):
            total += inputs[i] * self.weights[i]

        total += self.bias

        return total

    def predict(self, inputs):
        return self.weighted_sum(inputs)