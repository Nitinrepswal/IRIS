class DecisionTree:
    def __init__(self):
        self.threshold = None
        self.left_class = None
        self.right_class = None

    def gini_impurity(self, labels):
        if len(labels) == 0:
            return 0.0

        counts = {}

        for label in labels:
            if label not in counts:
                counts[label] = 0

            counts[label] += 1

        impurity = 1.0

        for count in counts.values():
            probability = count / len(labels)
            impurity -= probability ** 2

        return impurity

    def find_best_split(self, features, labels):
        best_threshold = None
        best_gini = float("inf")

        unique_features = sorted(set(features))

        for threshold in unique_features:
            left_labels = []
            right_labels = []

            for i in range(len(features)):
                if features[i] < threshold:
                    left_labels.append(labels[i])
                else:
                    right_labels.append(labels[i])

            if len(left_labels) == 0 or len(right_labels) == 0:
                continue

            left_gini = self.gini_impurity(left_labels)
            right_gini = self.gini_impurity(right_labels)

            total = len(features)

            weighted_gini = (
                (len(left_labels) / total) * left_gini
                + (len(right_labels) / total) * right_gini
            )

            if weighted_gini < best_gini:
                best_gini = weighted_gini
                best_threshold = threshold

        return best_threshold

    def fit(self, features, labels):
        self.threshold = self.find_best_split(features, labels)

        left_labels = []
        right_labels = []

        for i in range(len(features)):
            if features[i] < self.threshold:
                left_labels.append(labels[i])
            else:
                right_labels.append(labels[i])

        self.left_class = self.majority_class(left_labels)
        self.right_class = self.majority_class(right_labels)

    def majority_class(self, labels):
        counts = {}

        for label in labels:
            counts[label] = counts.get(label, 0) + 1

        return max(counts, key=counts.get)

    def predict_one(self, value):
        if value < self.threshold:
            return self.left_class

        return self.right_class

    def predict(self, values):
        predictions = []

        for value in values:
            predictions.append(self.predict_one(value))

        return predictions