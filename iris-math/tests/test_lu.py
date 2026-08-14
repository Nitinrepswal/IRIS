from lu import lu_decomposition


A = [
    [2, 1],
    [4, 3]
]

L, U = lu_decomposition(A)

print("L:")
for row in L:
    print(row)

print("U:")
for row in U:
    print(row)