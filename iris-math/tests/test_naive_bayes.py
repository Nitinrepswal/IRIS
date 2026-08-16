from naive_bayes import GaussianNaiveBayes


features = [1, 2, 3, 7, 8, 9]
labels = [0, 0, 0, 1, 1, 1]

model = GaussianNaiveBayes()

model.fit(features, labels)

predictions = model.predict([2, 5, 8])

print("Features:", features)
print("Labels:", labels)
print("Predictions:", predictions)