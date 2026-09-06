import torch
import torch.nn.functional as F


documents = [
    "Python is a high-level programming language.",
    "Machine learning allows computers to learn patterns from data.",
    "Deep learning uses neural networks to learn complex patterns.",
    "Transformers are neural network architectures based on attention.",
    "Vector databases store embeddings and support similarity search."
]


vocabulary = {
    "python": 0,
    "programming": 1,
    "language": 2,
    "machine": 3,
    "learning": 4,
    "computers": 5,
    "patterns": 6,
    "data": 7,
    "deep": 8,
    "neural": 9,
    "networks": 10,
    "transformers": 11,
    "attention": 12,
    "vector": 13,
    "databases": 14,
    "store": 15,
    "embeddings": 16,
    "similarity": 17,
    "search": 18
}


embedding = torch.nn.Embedding(len(vocabulary), 8)


def text_to_vector(text):
    words = text.lower().replace(".", "").split()

    ids = [
        vocabulary[word]
        for word in words
        if word in vocabulary
    ]

    ids = torch.tensor(ids)

    return embedding(ids).mean(dim=0)


document_vectors = torch.stack([
    text_to_vector(document)
    for document in documents
])


def retrieve(query, top_k=2):
    query_vector = text_to_vector(query)

    similarities = F.cosine_similarity(
        query_vector.unsqueeze(0),
        document_vectors
    )

    values, indices = torch.topk(similarities, top_k)

    results = []

    for value, index in zip(values, indices):
        results.append({
            "document": documents[index],
            "score": value.item()
        })

    return results


query = "machine learning"

results = retrieve(query, top_k=2)

print("Query:")
print(query)

print("\nRetrieved documents:")

for result in results:
    print(f"Document: {result['document']}")
    print(f"Similarity: {result['score']:.4f}")
    print("-" * 40)