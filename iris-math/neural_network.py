class NeuralNetwork:
    def __init__(self):
        self.weights_hidden = [
            [0.5, 0.2],
            [0.3, 0.4]
        ]

        self.bias_hidden = [0.1, 0.1]

        self.weights_output = [0.6, 0.7]

        self.bias_output = 0.1

    def forward(self, inputs):
        hidden_outputs = []

        for i in range(len(self.weights_hidden)):
            total = 0.0

            for j in range(len(inputs)):
                total += inputs[j] * self.weights_hidden[i][j]

            total += self.bias_hidden[i]

            hidden_outputs.append(total)

        output = 0.0

        for i in range(len(hidden_outputs)):
            output += (
                hidden_outputs[i] *
                self.weights_output[i]
            )

        output += self.bias_output

        return hidden_outputs, output