import torch
import torch.nn as nn


torch.manual_seed(42)

embedding_size = 8
num_heads = 2
sequence_length = 5
batch_size = 1

x = torch.randn(batch_size, sequence_length, embedding_size)

print("Input shape:")
print(x.shape)

transformer_layer = nn.TransformerEncoderLayer(
    d_model=embedding_size,
    nhead=num_heads,
    batch_first=True
)

transformer = nn.TransformerEncoder(
    transformer_layer,
    num_layers=2
)

output = transformer(x)

print("\nTransformer output shape:")
print(output.shape)

print("\nInput:")
print(x)

print("\nTransformer output:")
print(output)