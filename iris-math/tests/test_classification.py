from classification import BinaryClassifier


probabilities = [0.1, 0.3, 0.5, 0.7, 0.9]

classifier = BinaryClassifier()

predictions = classifier.predict(probabilities)

print("Probabilities:", probabilities)
print("Predictions:", predictions)