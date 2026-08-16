class GradientDescent:
    def __init__(self, learning_rate=0.01, iterations=1000):
        self.learning_rate = learning_rate
        self.iterations = iterations
        self.m = 0.0
        self.b = 0.0

    def fit(self, x, y):
        n = len(x)

        for _ in range(self.iterations):
            dm = 0.0
            db = 0.0

            for i in range(n):
                prediction = self.m * x[i] + self.b
                error = prediction - y[i]

                dm += error * x[i]
                db += error

            dm = (2 / n) * dm
            db = (2 / n) * db

            self.m -= self.learning_rate * dm
            self.b -= self.learning_rate * db

    def predict(self, x):
        predictions = []

        for value in x:
            predictions.append(self.m * value + self.b)

        return predictions