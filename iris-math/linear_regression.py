class LinearRegression:
    def __init__(self):
        self.m = 0.0
        self.b = 0.0

    def fit(self, x, y):
        n = len(x)

        x_mean = sum(x) / n
        y_mean = sum(y) / n

        numerator = 0.0
        denominator = 0.0

        for i in range(n):
            numerator += (x[i] - x_mean) * (y[i] - y_mean)
            denominator += (x[i] - x_mean) ** 2

        self.m = numerator / denominator
        self.b = y_mean - self.m * x_mean

    def predict(self, x):
        predictions = []

        for value in x:
            prediction = self.m * value + self.b
            predictions.append(prediction)

        return predictions