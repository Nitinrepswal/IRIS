def l1_penalty(weights, strength):
    penalty = 0.0

    for weight in weights:
        penalty += abs(weight)

    return strength * penalty


def l2_penalty(weights, strength):
    penalty = 0.0

    for weight in weights:
        penalty += weight ** 2

    return strength * penalty