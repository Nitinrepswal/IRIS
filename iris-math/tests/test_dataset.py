from dataset import Dataset


features = [
    [2, 60],
    [4, 75],
    [6, 85],
    [1, 50]
]

labels = [
    "Fail",
    "Pass",
    "Pass",
    "Fail"
]

dataset = Dataset(features, labels)

print("Number of samples:", len(dataset))

train, test = dataset.train_test_split(test_size=0.25)

print("Training samples:", len(train))
print("Testing samples:", len(test))

print("Training features:", train.get_features())
print("Testing features:", test.get_features())

print("Training labels:", train.get_labels())
print("Testing labels:", test.get_labels())