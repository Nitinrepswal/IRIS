class Neuron:
    def __init__(self, weights, bias):
        self.weights = weights
        self.bias = bias

    def forward(self, inputs):
        if len(inputs) != len(self.weights):
            raise ValueError("Inputs and weights must have the same length")

        weighted_sum = 0.0

        for i in range(len(inputs)):
            weighted_sum += inputs[i] * self.weights[i]

        weighted_sum += self.bias

        return weighted_sum