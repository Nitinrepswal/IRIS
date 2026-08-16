import math


class GaussianNaiveBayes:
    def __init__(self):
        self.classes = []
        self.means = {}
        self.variances = {}
        self.priors = {}

    def fit(self, x, y):
        self.classes = sorted(set(y))

        for class_value in self.classes:
            class_data = []

            for i in range(len(x)):
                if y[i] == class_value:
                    class_data.append(x[i])

            mean = sum(class_data) / len(class_data)

            variance = sum(
                (value - mean) ** 2
                for value in class_data
            ) / len(class_data)

            self.means[class_value] = mean
            self.variances[class_value] = variance
            self.priors[class_value] = len(class_data) / len(x)

    def gaussian_probability(self, value, mean, variance):
        if variance == 0:
            variance = 1e-9

        exponent = math.exp(
            -((value - mean) ** 2) / (2 * variance)
        )

        return (
            1 / math.sqrt(2 * math.pi * variance)
        ) * exponent

    def predict_one(self, value):
        probabilities = {}

        for class_value in self.classes:
            likelihood = self.gaussian_probability(
                value,
                self.means[class_value],
                self.variances[class_value]
            )

            probabilities[class_value] = (
                likelihood * self.priors[class_value]
            )

        return max(
            probabilities,
            key=probabilities.get
        )

    def predict(self, values):
        predictions = []

        for value in values:
            predictions.append(
                self.predict_one(value)
            )

        return predictions