from solve import solve_system


matrix = [
    [2, 1, 5],
    [1, 1, 3]
]

result = solve_system(matrix)

print("Unique:", result)
assert result == [2.0, 1.0]


matrix = [
    [1, 1, 3],
    [1, 1, 5]
]

result = solve_system(matrix)

print("No solution:", result)
assert result is None


matrix = [
    [1, 1, 3],
    [2, 2, 6]
]

result = solve_system(matrix)

print("Infinite:", result)
assert result == "infinite"


print("All tests passed!")