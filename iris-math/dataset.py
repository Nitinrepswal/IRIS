class Dataset:
    def __init__(self, features, labels):
        if len(features) != len(labels):
            raise ValueError("Features and labels must have the same length")

        self.features = features
        self.labels = labels

    def __len__(self):
        return len(self.features)

    def get_features(self):
        return self.features

    def get_labels(self):
        return self.labels

    def train_test_split(self, test_size=0.2):
        if not 0 < test_size < 1:
            raise ValueError("test_size must be between 0 and 1")

        split_index = int(len(self.features) * (1 - test_size))

        train_features = self.features[:split_index]
        test_features = self.features[split_index:]

        train_labels = self.labels[:split_index]
        test_labels = self.labels[split_index:]

        return (
            Dataset(train_features, train_labels),
            Dataset(test_features, test_labels)
        )