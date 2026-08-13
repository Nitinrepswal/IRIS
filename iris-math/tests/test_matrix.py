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


# invalid addition
Z = Matrix([
    [1, 2, 3],
    [4, 5, 6]
])

try:
    print("Invalid Add:", X + Z)
except ValueError as e:
    print("Invalid Add:", e)


# invalid subtraction
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


# matrix × vector
v = Vector([5, 6])

print("Matrix × Vector:", X * v)


# invalid matrix × vector
wrong_vector = Vector([1, 2, 3])

try:
    print("Invalid Matrix × Vector:", X * wrong_vector)
except ValueError as e:
    print("Invalid Matrix × Vector:", e)


# matrix × matrix
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


# determinant
D = Matrix([
    [2, 3],
    [1, 4]
])

print("Determinant:", D.determinant())


# 3×3 determinant
E3 = Matrix([
    [1, 2, 3],
    [0, 1, 4],
    [5, 6, 0]
])

print("3×3 Determinant:", E3.determinant())


# invalid determinant
try:
    print("Invalid Determinant:", B.determinant())
except ValueError as e:
    print("Invalid Determinant:", e)


# minor
minor_test = Matrix([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])

print("Minor:", minor_test.minor(1, 1))
print("Minor Determinant:", minor_test.minor(1, 1).determinant())


# cofactor
print("Cofactor:", minor_test.cofactor(0, 1))


# cofactor matrix
cofactor_test = Matrix([
    [1, 2, 3],
    [0, 1, 4],
    [5, 6, 0]
])

print("Cofactor Matrix:", cofactor_test.cofactor_matrix())


# adjugate
print("Adjugate:", cofactor_test.adjugate())


# inverse
inverse_test = Matrix([
    [2, 3],
    [1, 4]
])

print("Inverse:", inverse_test.inverse())


# inverse verification
identity_result = inverse_test * inverse_test.inverse()

print("Inverse Check:", identity_result)


# singular matrix
singular = Matrix([
    [1, 2],
    [2, 4]
])

print("Singular Determinant:", singular.determinant())

try:
    print("Singular Inverse:", singular.inverse())
except ValueError as e:
    print("Singular Error:", e)


# solve AX = B
solve_matrix = Matrix([
    [2, 3],
    [1, 4]
])

solve_vector = Vector([8, 9])

solution = solve_matrix.solve(solve_vector)

print("Solution:", solution)


# verify solution
print("Solution Check:", solve_matrix * solution)


# invalid solve
try:
    wrong_solution = Vector([1, 2, 3])
    print("Invalid Solution:", solve_matrix.solve(wrong_solution))
except ValueError as e:
    print("Invalid Solution:", e)