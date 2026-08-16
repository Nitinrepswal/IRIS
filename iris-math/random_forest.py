import random

from decision_tree import DecisionTree


class RandomForest:
    def __init__(self, n_trees=5):
        self.n_trees = n_trees
        self.trees = []

    def bootstrap_sample(self, features, labels):
        sample_features = []
        sample_labels = []

        for _ in range(len(features)):
            index = random.randrange(len(features))

            sample_features.append(features[index])
            sample_labels.append(labels[index])

        return sample_features, sample_labels

    def fit(self, features, labels):
        self.trees = []

        for _ in range(self.n_trees):
            sample_features, sample_labels = self.bootstrap_sample(
                features,
                labels
            )

            tree = DecisionTree()

            tree.fit(sample_features, sample_labels)

            self.trees.append(tree)

    def predict_one(self, value):
        predictions = []

        for tree in self.trees:
            predictions.append(tree.predict_one(value))

        votes = {}

        for prediction in predictions:
            votes[prediction] = votes.get(prediction, 0) + 1

        return max(votes, key=votes.get)

    def predict(self, values):
        predictions = []

        for value in values:
            predictions.append(self.predict_one(value))

        return predictions