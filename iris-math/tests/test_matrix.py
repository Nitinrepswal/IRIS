from matrix import Matrix
from vector import Vector


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
    Matrix([
        [1, 2, 3],
        [4, 5]
    ])
except ValueError as e:
    print("Invalid Matrix:", e)


# empty matrix
try:
    Matrix([])
except ValueError as e:
    print("Empty Matrix:", e)


# addition
X = Matrix([
    [1, 2],
    [3, 4]
])

Y = Matrix([
    [5, 6],
    [7, 8]
])

print("Add:", X + Y)


# subtraction
print("Sub:", X - Y)


# different shapes
Z = Matrix([
    [1, 2, 3],
    [4, 5, 6]
])

try:
    print("Invalid Add:", X + Z)
except ValueError as e:
    print("Invalid Add:", e)

try:
    print("Invalid Sub:", X - Z)
except ValueError as e:
    print("Invalid Sub:", e)


# scalar multiplication
print("Multiply:", X * 2)

# reverse multiplication
print("Reverse Multiply:", 2 * X)


# transpose
print("Transpose:", B.transpose())
print("Transpose Shape:", B.transpose().shape)

# transpose twice
print("Transpose Twice:", B.transpose().transpose())


# matrix * vector
v = Vector([5, 6])

print("Matrix × Vector:", X * v)


# invalid matrix * vector
wrong_vector = Vector([1, 2, 3])

try:
    print("Invalid Matrix × Vector:", X * wrong_vector)
except ValueError as e:
    print("Invalid Matrix × Vector:", e)


# matrix * matrix
M = Matrix([
    [1, 2],
    [3, 4]
])

N = Matrix([
    [5, 6],
    [7, 8]
])

print("Matrix Multiply:", M * N)


# invalid matrix multiplication
P = Matrix([
    [1, 2, 3]
])

try:
    print("Invalid Matrix Multiply:", M * P)
except ValueError as e:
    print("Invalid Matrix Multiply:", e)


# equality
E = Matrix([
    [1, 2],
    [3, 4]
])

F = Matrix([
    [1, 2],
    [3, 4]
])

G = Matrix([
    [1, 2],
    [3, 5]
])

print("Equal:", E == F)
print("Not Equal:", E == G)


# identity matrix
I = Matrix([
    [1, 0],
    [0, 1]
])

print("Identity Check:", M * I)
print("Identity Equal:", M * I == M)