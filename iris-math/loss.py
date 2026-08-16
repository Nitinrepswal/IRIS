class LossFunctions:

    def mean_squared_error(self, actual, predicted):
        if len(actual) != len(predicted):
            raise ValueError("Actual and predicted values must have the same length")

        total = 0.0

        for i in range(len(actual)):
            error = predicted[i] - actual[i]
            total += error ** 2

        return total / len(actual)