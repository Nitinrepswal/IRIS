import torch
import torch.nn.functional as F


class VectorDatabase:
    def __init__(self):
        self.documents = []
        self.vectors = []

    def add(self, document, vector):
        self.documents.append(document)
        self.vectors.append(vector)

    def search(self, query_vector, top_k=1):
        vectors = torch.stack(self.vectors)

        query_vector = query_vector.unsqueeze(0)

        similarities = F.cosine_similarity(
            query_vector,
            vectors
        )

        values, indices = torch.topk(similarities, top_k)

        results = []

        for value, index in zip(values, indices):
            results.append({
                "document": self.documents[index],
                "score": value.item()
            })

        return results


db = VectorDatabase()

db.add(
    "Python is a programming language.",
    torch.tensor([1.0, 0.0, 0.0, 0.0])
)

db.add(
    "Transformers use attention mechanisms.",
    torch.tensor([0.0, 1.0, 0.0, 0.0])
)

db.add(
    "Paris is the capital of France.",
    torch.tensor([0.0, 0.0, 1.0, 0.0])
)

query = torch.tensor([0.9, 0.1, 0.0, 0.0])

results = db.search(query, top_k=2)

print("Query vector:")
print(query)

print("\nSearch results:")

for result in results:
    print(f"Document: {result['document']}")
    print(f"Similarity: {result['score']:.4f}")
    print("-" * 40)