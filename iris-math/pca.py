import math


def mean(values):
    return sum(values) / len(values)


def center_data(data):
    means = [
        mean([row[j] for row in data])
        for j in range(len(data[0]))
    ]

    return [
        [row[j] - means[j] for j in range(len(row))]
        for row in data
    ]


def covariance_matrix(data):
    centered = center_data(data)
    rows = len(centered)
    cols = len(centered[0])

    return [
        [
            sum(centered[k][i] * centered[k][j] for k in range(rows)) / rows
            for j in range(cols)
        ]
        for i in range(cols)
    ]


def power_iteration(matrix, iterations=100):
    n = len(matrix)
    vector = [1.0] * n

    for _ in range(iterations):
        result = [
            sum(matrix[i][j] * vector[j] for j in range(n))
            for i in range(n)
        ]

        magnitude = math.sqrt(sum(value ** 2 for value in result))

        if magnitude == 0:
            break

        vector = [value / magnitude for value in result]

    return vector


def pca(data, components=1):
    centered = center_data(data)
    covariance = covariance_matrix(data)

    component = power_iteration(covariance)

    transformed = [
        [sum(row[j] * component[j] for j in range(len(row)))]
        for row in centered
    ]

    return transformed