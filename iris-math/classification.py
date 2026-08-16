class BinaryClassifier:
    def __init__(self, threshold=0.5):
        self.threshold = threshold

    def predict(self, probabilities):
        predictions = []

        for probability in probabilities:
            if probability >= self.threshold:
                predictions.append(1)
            else:
                predictions.append(0)

        return predictions