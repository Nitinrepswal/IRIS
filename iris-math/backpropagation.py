class SimpleNeuron:
    def __init__(self, weight=0.5, bias=0.0, learning_rate=0.1):
        self.weight = weight
        self.bias = bias
        self.learning_rate = learning_rate

    def forward(self, x):
        return self.weight * x + self.bias

    def train_step(self, x, target):
        # Forward pass
        prediction = self.forward(x)

        # Calculate error
        error = prediction - target

        # Mean squared error for one value
        loss = error ** 2

        # Gradients
        d_loss_d_prediction = 2 * error

        d_prediction_d_weight = x
        d_prediction_d_bias = 1

        d_loss_d_weight = (
            d_loss_d_prediction *
            d_prediction_d_weight
        )

        d_loss_d_bias = (
            d_loss_d_prediction *
            d_prediction_d_bias
        )

        # Update parameters
        self.weight -= (
            self.learning_rate *
            d_loss_d_weight
        )

        self.bias -= (
            self.learning_rate *
            d_loss_d_bias
        )

        return prediction, loss