import torch
import torch.nn.functional as F


documents = [
    "Python is a programming language.",
    "Transformers use attention mechanisms.",
    "Paris is the capital of France."
]

vocabulary = {
    "python": 0,
    "programming": 1,
    "language": 2,
    "transformers": 3,
    "attention": 4,
    "paris": 5,
    "capital": 6,
    "france": 7
}

embedding = torch.nn.Embedding(len(vocabulary), 4)


def text_to_vector(text):
    words = text.lower().replace(".", "").split()

    ids = [
        vocabulary[word]
        for word in words
        if word in vocabulary
    ]

    ids = torch.tensor(ids)

    vectors = embedding(ids)

    return vectors.mean(dim=0)


document_vectors = torch.stack([
    text_to_vector(document)
    for document in documents
])

query = "Python programming language"
query_vector = text_to_vector(query)

similarities = F.cosine_similarity(
    query_vector.unsqueeze(0),
    document_vectors
)

print("Query:")
print(query)

print("\nQuery vector:")
print(query_vector)

print("\nSimilarities:")

for document, similarity in zip(documents, similarities):
    print(f"Document: {document}")
    print(f"Similarity: {similarity.item():.4f}")
    print("-" * 40)

best_index = torch.argmax(similarities)

print("\nMost similar document:")
print(documents[best_index])