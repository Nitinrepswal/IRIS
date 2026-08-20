import torch
import torch.nn as nn
import torch.nn.functional as F


torch.manual_seed(42)

batch_size = 1
sequence_length = 4
embedding_dimension = 8
num_heads = 2
head_dimension = embedding_dimension // num_heads

x = torch.randn(
    batch_size,
    sequence_length,
    embedding_dimension
)

Wq = nn.Linear(embedding_dimension, embedding_dimension)
Wk = nn.Linear(embedding_dimension, embedding_dimension)
Wv = nn.Linear(embedding_dimension, embedding_dimension)

Wo = nn.Linear(embedding_dimension, embedding_dimension)

Q = Wq(x)
K = Wk(x)
V = Wv(x)

Q = Q.view(
    batch_size,
    sequence_length,
    num_heads,
    head_dimension
)

K = K.view(
    batch_size,
    sequence_length,
    num_heads,
    head_dimension
)

V = V.view(
    batch_size,
    sequence_length,
    num_heads,
    head_dimension
)

Q = Q.transpose(1, 2)
K = K.transpose(1, 2)
V = V.transpose(1, 2)

scores = Q @ K.transpose(-2, -1)

scores = scores / (head_dimension ** 0.5)

attention_weights = F.softmax(scores, dim=-1)

head_outputs = attention_weights @ V

head_outputs = head_outputs.transpose(1, 2)

combined = head_outputs.contiguous().view(
    batch_size,
    sequence_length,
    embedding_dimension
)

output = Wo(combined)

print("Input shape:")
print(x.shape)

print("\nQ shape:")
print(Q.shape)

print("\nK shape:")
print(K.shape)

print("\nV shape:")
print(V.shape)

print("\nAttention weights shape:")
print(attention_weights.shape)

print("\nHead outputs shape:")
print(head_outputs.shape)

print("\nCombined shape:")
print(combined.shape)

print("\nFinal output shape:")
print(output.shape)

print("\nAttention weights:")
print(attention_weights)

print("\nFinal output:")
print(output)