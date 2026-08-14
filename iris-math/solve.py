def solve_system(matrix):
    a = [row[:] for row in matrix]

    rows = len(a)
    cols = len(a[0])
    variables = cols - 1

    pivot_row = 0

    # Find pivots
    for col in range(variables):
        pivot = None

        for row in range(pivot_row, rows):
            if abs(a[row][col]) > 1e-10:
                pivot = row
                break

        if pivot is None:
            continue

        # Swap rows
        a[pivot_row], a[pivot] = a[pivot], a[pivot_row]

        # Make pivot 1
        pivot_value = a[pivot_row][col]

        for j in range(col, cols):
            a[pivot_row][j] /= pivot_value

        # Eliminate the column
        for row in range(rows):
            if row == pivot_row:
                continue

            factor = a[row][col]

            for j in range(col, cols):
                a[row][j] -= factor * a[pivot_row][j]

        pivot_row += 1

    # Check for no solution
    for row in a:
        if all(abs(x) < 1e-10 for x in row[:-1]):
            if abs(row[-1]) > 1e-10:
                return None

    # Find rank
    rank = 0

    for row in a:
        if any(abs(x) > 1e-10 for x in row[:-1]):
            rank += 1

    # Check for infinite solutions
    if rank < variables:
        return "infinite"

    # Get the solution
    solution = [0.0] * variables

    for row in a:
        for col in range(variables):
            if abs(row[col] - 1) < 1e-10:
                solution[col] = row[-1]
                break

    return solution