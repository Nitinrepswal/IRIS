import torch
import torch.nn as nn


# Vocabulary
vocabulary = {
    "cat": 0,
    "dog": 1,
    "king": 2,
    "queen": 3,
    "apple": 4
}


# Create embedding layer
embedding = nn.Embedding(
    num_embeddings=5,
    embedding_dim=4
)


# Convert words into token IDs
tokens = torch.tensor([
    vocabulary["cat"],
    vocabulary["dog"],
    vocabulary["king"]
])


print("Token IDs:")
print(tokens)


# Get embeddings
vectors = embedding(tokens)


print("\nEmbeddings:")
print(vectors)


print("\nEmbedding shape:")
print(vectors.shape)