class KNearestNeighbors:
    def __init__(self, k=3):
        self.k = k
        self.features = []
        self.labels = []

    def fit(self, features, labels):
        self.features = features
        self.labels = labels

    def predict_one(self, value):
        distances = []

        for i in range(len(self.features)):
            distance = abs(value - self.features[i])
            distances.append((distance, self.labels[i]))

        distances.sort()

        nearest_neighbors = distances[:self.k]

        votes = {}

        for _, label in nearest_neighbors:
            if label not in votes:
                votes[label] = 0

            votes[label] += 1

        return max(votes, key=votes.get)

    def predict(self, values):
        predictions = []

        for value in values:
            predictions.append(self.predict_one(value))

        return predictions