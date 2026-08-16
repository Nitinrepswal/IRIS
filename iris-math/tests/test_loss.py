from loss import LossFunctions


actual = [2, 4, 6]
predicted = [3, 5, 5]

loss = LossFunctions()

mse = loss.mean_squared_error(actual, predicted)

print("Actual:", actual)
print("Predicted:", predicted)
print("Mean Squared Error:", mse)