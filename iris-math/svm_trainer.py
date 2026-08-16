class SVMTrainer:
    def __init__(self, learning_rate=0.01, epochs=100):
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.weight = 0.0
        self.bias = 0.0

    def fit(self, features, labels):
        for label_index in range(len(labels)):
            if labels[label_index] == 0:
                labels[label_index] = -1

        for _ in range(self.epochs):
            for i in range(len(features)):
                x = features[i]
                y = labels[i]

                margin = y * (self.weight * x + self.bias)

                if margin >= 1:
                    self.weight -= (
                        self.learning_rate * 2 * self.weight
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