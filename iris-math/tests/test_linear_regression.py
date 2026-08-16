from linear_regression import LinearRegression


x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]

model = LinearRegression()

model.fit(x, y)

predictions = model.predict([6, 7, 8])

print("Slope:", model.m)
print("Intercept:", model.b)
print("Predictions:", predictions)