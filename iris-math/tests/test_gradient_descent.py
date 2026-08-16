from gradient_descent import GradientDescent


x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]

model = GradientDescent(
    learning_rate=0.01,
    iterations=1000
)

model.fit(x, y)

predictions = model.predict([6, 7, 8])

print("Learned slope:", model.m)
print("Learned intercept:", model.b)
print("Predictions:", predictions)