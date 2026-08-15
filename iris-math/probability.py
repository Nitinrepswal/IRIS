def probability(favorable, total):
    if total <= 0:
        raise ValueError("Total outcomes must be positive")

    if favorable < 0 or favorable > total:
        raise ValueError("Invalid favorable outcomes")

    return favorable / total


def expected_value(values, probabilities):
    if len(values) != len(probabilities):
        raise ValueError("Values and probabilities must have the same length")

    return sum(
        value * probability
        for value, probability in zip(values, probabilities)
    )


def variance(values, probabilities):
    mean = expected_value(values, probabilities)

    return sum(
        probability * (value - mean) ** 2
        for value, probability in zip(values, probabilities)
    )


def conditional_probability(joint, given):
    if given <= 0:
        raise ValueError("Given probability must be positive")

    return joint / given


def bayes(prior, likelihood, evidence):
    if evidence <= 0:
        raise ValueError("Evidence probability must be positive")

    return (likelihood * prior) / evidence