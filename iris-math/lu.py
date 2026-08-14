def lu_decomposition(matrix):
    n = len(matrix)

    L = [[0.0] * n for _ in range(n)]
    U = [row[:] for row in matrix]

    for i in range(n):
        L[i][i] = 1.0

    for i in range(n):
        for j in range(i + 1, n):
            factor = U[j][i] / U[i][i]

            L[j][i] = factor

            for k in range(i, n):
                U[j][k] -= factor * U[i][k]

    return L, U