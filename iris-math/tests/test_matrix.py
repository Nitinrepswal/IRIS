from matrix import Matrix


# basic matrix
A = Matrix([
    [1, 2],
    [3, 4]
])

print("Matrix:", A)
print("Shape:", A.shape)


# rectangular matrix
B = Matrix([
    [1, 2, 3],
    [4, 5, 6]
])

print("Matrix:", B)
print("Shape:", B.shape)


# invalid matrix
try:
    C = Matrix([
        [1, 2, 3],
        [4, 5]
    ])
except ValueError as e:
    print("Invalid Matrix:", e)


# empty matrix
try:
    D = Matrix([])
except ValueError as e:
    print("Empty Matrix:", e)
