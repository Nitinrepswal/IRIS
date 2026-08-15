import math

def mean(values):
    return sum(values) / len(values)


def covariance(x, y):
    if len(x) != len(y):
        raise ValueError("Lists must have the same length")

    x_mean = mean(x)
    y_mean = mean(y)

    return sum(
        (x[i] - x_mean) * (y[i] - y_mean)
        for i in range(len(x))
    ) / len(x)


def correlation(x, y):
    if len(x) != len(y):
        raise ValueError("Lists must have the same length")

    x_mean = mean(x)
    y_mean = mean(y)

    numerator = sum(
        (x[i] - x_mean) * (y[i] - y_mean)
        for i in range(len(x))
    )

    x_spread = math.sqrt(
        sum((value - x_mean) ** 2 for value in x)
    )

    y_spread = math.sqrt(
        sum((value - y_mean) ** 2 for value in y)
    )

    if x_spread == 0 or y_spread == 0:
        raise ValueError("Correlation is undefined")

    return numerator / (x_spread * y_spread)