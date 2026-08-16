from decision_tree import DecisionTree

features = [1, 2, 3, 7, 8, 9]
labels = [0, 0, 0, 1, 1, 1]

model = DecisionTree()

model.fit(features, labels)

predictions = model.predict([2, 5, 8])

print("Features:", features)
print("Labels:", labels)
print("Best threshold:", model.threshold)
print("Predictions:", predictions)