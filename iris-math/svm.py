class LinearSVM:
    def __init__(self, learning_rate=0.01, epochs=1000):
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.weight = 0.0
        self.bias = 0.0

    def fit(self, features, labels):
        converted_labels = []

        for label in labels:
            if label == 0:
                converted_labels.append(-1)
            else:
                converted_labels.append(1)

        for _ in range(self.epochs):
            for i in range(len(features)):
                x = features[i]
                y = converted_labels[i]

                condition = y * (self.weight * x + self.bias)

                if condition >= 1:
                    self.weight -= self.learning_rate * (
                        2 * self.weight
                    )
                else:
                    self.weight -= self.learning_rate * (
                        2 * self.weight - y * x
                    )

                    self.bias -= self.learning_rate * (-y)

    def predict_one(self, value):
        score = self.weight * value + self.bias

        if score >= 0:
            return 1

        return 0

    def predict(self, values):
        predictions = []

        for value in values:
            predictions.append(self.predict_one(value))

        return predictions