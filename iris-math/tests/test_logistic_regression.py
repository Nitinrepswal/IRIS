from logistic_regression import LogisticRegression


x = [1, 2, 3, 7, 8, 9]
y = [0, 0, 0, 1, 1, 1]

model = LogisticRegression(
    learning_rate=0.1,
    iterations=1000
)

model.fit(x, y)

probabilities = model.predict_probability([2, 5, 8])

predictions = model.predict([2, 5, 8])

print("Probabilities:", probabilities)
print("Predictions:", predictions)