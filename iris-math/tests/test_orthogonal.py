from orthogonal import gram_schmidt, dot


vectors = [
    [1, 1],
    [1, 0]
]

result = gram_schmidt(vectors)

print("Result:")

for vector in result:
    print(vector)

assert abs(dot(result[0], result[1])) < 1e-10

print("Orthogonalization passed!")