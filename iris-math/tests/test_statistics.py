from statistics import (
    mean,
    median,
    mode,
    data_range,
    variance,
    standard_deviation
)


values = [2, 4, 4, 6, 8]

print("Mean:", mean(values))
print("Median:", median(values))
print("Mode:", mode(values))
print("Range:", data_range(values))
print("Variance:", variance(values))
print("Standard deviation:", standard_deviation(values))