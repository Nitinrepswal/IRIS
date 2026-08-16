from scaling import MinMaxScaler, StandardScaler


data = [
    [10, 100],
    [20, 200],
    [30, 300],
    [40, 400]
]


print("Original data:")
print(data)


minmax = MinMaxScaler()

minmax_result = minmax.fit_transform(data)

print("\nMin-Max scaled:")
for row in minmax_result:
    print(row)


standard = StandardScaler()

standard_result = standard.fit_transform(data)

print("\nStandardized:")
for row in standard_result:
    print(row)