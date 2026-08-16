from knn import KNearestNeighbors


features = [1, 2, 3, 7, 8, 9]
labels = [0, 0, 0, 1, 1, 1]

model = KNearestNeighbors(k=3)

model.fit(features, labels)

predictions = model.predict([2, 5, 8])

print("Features:", features)
print("Labels:", labels)
print("Predictions:", predictions)