from activations import relu


class ForwardNetwork:
    def __init__(self):
        self.hidden_weights = [
            [0.5, 0.2],
            [0.3, 0.4]
        ]

        self.hidden_biases = [0.1, 0.1]

        self.output_weights = [0.6, 0.7]

        self.output_bias = 0.1

    def forward(self, inputs):
        hidden_outputs = []

        # Hidden layer
        for i in range(len(self.hidden_weights)):
            weighted_sum = 0.0

            for j in range(len(inputs)):
                weighted_sum += (
                    inputs[j] *
                    self.hidden_weights[i][j]
                )

            weighted_sum += self.hidden_biases[i]

            activated = relu(weighted_sum)

            hidden_outputs.append(activated)

        # Output layer
        output_sum = 0.0

        for i in range(len(hidden_outputs)):
            output_sum += (
                hidden_outputs[i] *
                self.output_weights[i]
            )

        output_sum += self.output_bias

        output = relu(output_sum)

        return hidden_outputs, output