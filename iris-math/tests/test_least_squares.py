from least_squares import least_squares

A = [
    [1, 1],
    [2, 1],
    [3, 1]
]

b = [2, 3, 5]

result = least_squares(A, b)

print("Best-fit coefficients:", result)