from solve import solve_system


def least_squares(A, b):
    At = [list(row) for row in zip(*A)]

    AtA = [
        [
            sum(At[i][k] * A[k][j] for k in range(len(A)))
            for j in range(len(A[0]))
        ]
        for i in range(len(At))
    ]

    Atb = [
        sum(At[i][k] * b[k] for k in range(len(A)))
        for i in range(len(At))
    ]

    augmented = [
        AtA[i] + [Atb[i]]
        for i in range(len(AtA))
    ]

    return solve_system(augmented)