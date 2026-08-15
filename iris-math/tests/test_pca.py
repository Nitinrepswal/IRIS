from pca import pca

data = [
    [2, 1],
    [3, 2],
    [4, 3],
    [5, 4],
    [6, 5]
]

result = pca(data)

print("PCA result:")

for row in result:
    print(row)