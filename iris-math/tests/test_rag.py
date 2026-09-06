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
    words = (
        text.lower()
        .replace(".", "")
        .replace(",", "")
        .replace("?", "")
        .replace("!", "")
    ).split()

    ids = [
        vocabulary[word]
        for word in words
        if word in vocabulary
    ]

    if not ids:
        return torch.zeros(8)

    ids = torch.tensor(ids, dtype=torch.long)

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


def generate_answer(question, context):
    question = question.lower()

    if "python" in question:
        return "Python is a high-level programming language."

    if "transformer" in question:
        return "Transformers are neural network architectures based on attention."

    if "machine learning" in question:
        return "Machine learning allows computers to learn patterns from data."

    if "vector database" in question:
        return "Vector databases store embeddings and support similarity search."

    return f"Based on the retrieved context: {context[0]}"


question = "What is Python?"

results = retrieve(question, top_k=2)

context = [
    result["document"]
    for result in results
]


prompt = f"""
You are IRIS, a helpful AI assistant.

Use the following retrieved context to answer the question.

Context:
{chr(10).join(context)}

Question:
{question}

Answer:
"""


answer = generate_answer(question, context)


print("Question:")
print(question)

print("\nRetrieved context:")

for item in context:
    print(f"- {item}")

print("\nRAG Prompt:")
print(prompt)

print("IRIS:")
print(answer)