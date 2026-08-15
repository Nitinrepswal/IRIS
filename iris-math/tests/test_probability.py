from probability import (
    probability,
    expected_value,
    variance,
    conditional_probability,
    bayes
)


print("Probability:", probability(3, 6))

values = [0, 1]
probabilities = [0.5, 0.5]

print("Expected value:", expected_value(values, probabilities))
print("Variance:", variance(values, probabilities))

print("Conditional probability:", conditional_probability(1, 3))

print("Bayes:", bayes(0.2, 0.5, 0.4))