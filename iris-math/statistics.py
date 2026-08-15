import math


def mean(values):
    if not values:
        raise ValueError("Values cannot be empty")

    return sum(values) / len(values)


def median(values):
    if not values:
        raise ValueError("Values cannot be empty")

    data = sorted(values)
    n = len(data)

    if n % 2 == 1:
        return data[n // 2]

    return (data[n // 2 - 1] + data[n // 2]) / 2


def mode(values):
    if not values:
        raise ValueError("Values cannot be empty")

    counts = {}

    for value in values:
        counts[value] = counts.get(value, 0) + 1

    return max(counts, key=counts.get)


def data_range(values):
    if not values:
        raise ValueError("Values cannot be empty")

    return max(values) - min(values)


def variance(values):
    avg = mean(values)

    return sum(
        (value - avg) ** 2
        for value in values
    ) / len(values)


def standard_deviation(values):
    return math.sqrt(variance(values))