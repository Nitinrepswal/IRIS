import torch
import torch.nn as nn


torch.manual_seed(42)


class TransformerBlock(nn.Module):
    def __init__(self, embedding_dimension, num_heads, feed_forward_dimension):
        super().__init__()

        self.attention = nn.MultiheadAttention(
            embed_dim=embedding_dimension,
            num_heads=num_heads,
            batch_first=True
        )

        self.norm1 = nn.LayerNorm(embedding_dimension)

        self.feed_forward = nn.Sequential(
            nn.Linear(embedding_dimension, feed_forward_dimension),
            nn.ReLU(),
            nn.Linear(feed_forward_dimension, embedding_dimension)
        )

        self.norm2 = nn.LayerNorm(embedding_dimension)

    def forward(self, x):
        attention_output, attention_weights = self.attention(
            x,
            x,
            x
        )

        x = self.norm1(x + attention_output)

        feed_forward_output = self.feed_forward(x)

        x = self.norm2(x + feed_forward_output)

        return x, attention_weights


batch_size = 1
sequence_length = 4
embedding_dimension = 8
num_heads = 2
feed_forward_dimension = 32

x = torch.randn(
    batch_size,
    sequence_length,
    embedding_dimension
)

transformer_block = TransformerBlock(
    embedding_dimension,
    num_heads,
    feed_forward_dimension
)

output, attention_weights = transformer_block(x)

print("Input shape:")
print(x.shape)

print("\nAttention weights shape:")
print(attention_weights.shape)

print("\nOutput shape:")
print(output.shape)

print("\nInput:")
print(x)

print("\nTransformer block output:")
print(output)