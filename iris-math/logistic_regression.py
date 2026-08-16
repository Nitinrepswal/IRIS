import math


class LogisticRegression:
    def __init__(self, learning_rate=0.1, iterations=1000):
        self.learning_rate = learning_rate
        self.iterations = iterations
        self.weight = 0.0
        self.bias = 0.0

    def sigmoid(self, z):
        return 1 / (1 + math.exp(-z))

    def fit(self, x, y):
        n = len(x)

        for _ in range(self.iterations):
            dw = 0.0
            db = 0.0

            for i in range(n):
                linear_output = self.weight * x[i] + self.bias
                prediction = self.sigmoid(linear_output)

                error = prediction - y[i]

                dw += error * x[i]
                db += error

            dw /= n
            db /= n

            self.weight -= self.learning_rate * dw
            self.bias -= self.learning_rate * db

    def predict_probability(self, x):
        probabilities = []

        for value in x:
            linear_output = self.weight * value + self.bias
            probability = self.sigmoid(linear_output)
            probabilities.append(probability)

        return probabilities

    def predict(self, x):
        probabilities = self.predict_probability(x)

        predictions = []

        for probability in probabilities:
            if probability >= 0.5:
                predictions.append(1)
            else:
                predictions.append(0)

        return predictions