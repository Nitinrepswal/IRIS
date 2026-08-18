import torch
import torch.nn as nn


torch.manual_seed(42)

vocabulary = {
    "IRIS": 0,
    "is": 1,
    "an": 2,
    "intelligent": 3,
    "AI": 4,
    "assistant": 5
}

text = "IRIS is an intelligent AI assistant"

tokens = text.split()
token_ids = torch.tensor([vocabulary[token] for token in tokens])

embedding = nn.Embedding(
    num_embeddings=len(vocabulary),
    embedding_dim=4
)

vectors = embedding(token_ids)

print("Tokens:")
print(tokens)

print("\nToken IDs:")
print(token_ids)

print("\nEmbedding shape:")
print(vectors.shape)

print("\nEmbeddings:")
print(vectors)