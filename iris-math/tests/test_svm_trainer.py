from svm_trainer import SVMTrainer


features = [1, 2, 3, 7, 8, 9]
labels = [0, 0, 0, 1, 1, 1]

model = SVMTrainer(
    learning_rate=0.001,
    epochs=1000
)

model.fit(features, labels)

predictions = model.predict([2, 5, 8])

print("Weight:", model.weight)
print("Bias:", model.bias)
print("Predictions:", predictions)