import torch
import torch.nn.functional as F


torch.manual_seed(42)

sequence_length = 3
embedding_dimension = 4

x = torch.randn(sequence_length, embedding_dimension)

Wq = torch.randn(embedding_dimension, embedding_dimension)
Wk = torch.randn(embedding_dimension, embedding_dimension)
Wv = torch.randn(embedding_dimension, embedding_dimension)

Q = x @ Wq
K = x @ Wk
V = x @ Wv

scores = Q @ K.T

scores = scores / (embedding_dimension ** 0.5)

attention_weights = F.softmax(scores, dim=-1)

output = attention_weights @ V

print("Input shape:")
print(x.shape)

print("\nQuery shape:")
print(Q.shape)

print("\nKey shape:")
print(K.shape)

print("\nValue shape:")
print(V.shape)

print("\nAttention scores:")
print(scores)

print("\nAttention weights:")
print(attention_weights)

print("\nRow sums:")
print(attention_weights.sum(dim=-1))

print("\nOutput shape:")
print(output.shape)

print("\nAttention output:")
print(output)