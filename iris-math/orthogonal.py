import math


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def norm(v):
    return math.sqrt(dot(v, v))


def projection(v, u):
    factor = dot(v, u) / dot(u, u)
    return [factor * x for x in u]


def gram_schmidt(vectors):
    result = []

    for v in vectors:
        u = v[:]

        for previous in result:
            proj = projection(v, previous)

            u = [
                u[i] - proj[i]
                for i in range(len(u))
            ]

        result.append(u)

    return result